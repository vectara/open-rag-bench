import os
import json
from typing import Any, Dict, List, Optional

from openai import OpenAI
from openai.types import FileObject
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run

from mistralai import Mistral

from tenacity import retry, stop_after_attempt, wait_random_exponential

class GPT4o:
    """
    A class to manage interactions with the GPT-4o service for generating extractive queries from uploaded files.

    Attributes:
        client (OpenAI): The OpenAI client instance initialized with an API key.
        model (str): The model name to be used for generating responses.
        file (Optional[FileObject]): The file object uploaded via the `upload` method.
        assistant (Optional[Assistant]): The assistant object created after file upload.
        thread (Optional[Thread]): The conversation thread object.
        run (Optional[Run]): The result object tracking the status of a generated thread run.
        prompt_for_extractive_query (str): The prompt template used to instruct the assistant.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        """
        Initialize the GPT4o instance with the specified model.

        Args:
            model (str): The model name for generating responses (default is "gpt-4o").
        """
        self.client: OpenAI = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model: str = model
        self.file: Optional[FileObject] = None
        self.assistant: Optional[Assistant] = None
        self.thread: Optional[Thread] = None
        self.run: Optional[Run] = None
        self._init_prompts()

    def upload(self, path: str) -> None:
        """
        Upload a file and create an associated assistant instance.

        Args:
            path (str): The filesystem path to the file to be uploaded.
        """
        self.file = self.client.files.create(
            file=open(path, 'rb'),
            purpose="assistants"
        )
        self.assistant = self.client.beta.assistants.create(
            instructions="You are an assistant that follows the user's instruction based on the attached file.",
            model=self.model,
            temperature=0,
            tools=[{"type": "code_interpreter"}],
            tool_resources={"code_interpreter": {"file_ids": [self.file.id]}}
        )

    def _init_prompts(self) -> None:
        """Initialize the prompt template for extractive query generation."""
        self.prompt_for_extractive_query: str = """
Your task is to write a list of 10 factoid questions and their answers given the text in the attached file.
Your factoid questions should be answerable with a specific, concise piece of factual information from the texts of the file.
Your factoid questions should be formulated in the same style as questions users could ask in a search engine.
This means that your extractive questions MUST NOT mention something like "according to the passage" or "context".
Your factoid questions MUST NOT be about the tables or figures in the file.
Your factoid questions MUST NOT be about the authors, publication date, or any other meta-information.

Provide your answer as follows:

Output:::
Question 1: (your factoid question)
Answer: (your answer to the factoid question)
Question 2: (your factoid question)
Answer: (your answer to the factoid question)
...
Question 10: (your factoid question)
Answer: (your answer to the factoid question)

Now, provide your factoid questions and answers based on the text in the attached file.
Output:::
"""

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self) -> str:
        """
        Generate factoid questions and answers using the assistant.

        Returns:
            str: a message containing the generated factoid questions and answers.

        Raises:
            Exception: If the generated run does not complete successfully.
        """
        # Create a new conversation thread
        self.thread = self.client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": self.prompt_for_extractive_query,
                "attachments": [{
                    "file_id": self.file.id,
                    "tools": [{"type": "code_interpreter"}]
                }]
            }]
        )

        # Poll for thread completion
        self.run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )

        # Retrieve messages upon successful completion
        if self.run.status == 'completed':
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            return messages.data[0].content[0].text.value
        else:
            raise Exception("Run failed to complete")


class MistralOCR:
    """A class to handle OCR operations using Mistral and OpenAI APIs.

    This class provides methods to upload a PDF file to the Mistral API, extract OCR data,
    and convert the extracted data to Markdown format with embedded image data.
    """

    def __init__(self, mistral_api_key: str = None, openai_api_key: str = None) -> None:
        """Initializes the MistralOCR instance with API keys.

        If API keys are not provided, the keys are retrieved from environment variables.

        Args:
            mistral_api_key (str, optional): API key for Mistral. Defaults to None.
            openai_api_key (str, optional): API key for OpenAI. Defaults to None.
        """
        self.mistral_client = Mistral(api_key=mistral_api_key if mistral_api_key else os.environ.get("MISTRAL_API_KEY"))
        self.openai_client = OpenAI(api_key=openai_api_key if openai_api_key else os.environ.get("OPENAI_API_KEY"))

    ###### Mistral OCR methods ######
    def upload(self, path: str) -> None:
        """Uploads a PDF file to the Mistral API for OCR processing.

        Args:
            path (str): The file path of the PDF to be uploaded.
        """
        self.uploaded_pdf = self.mistral_client.files.upload(
            file={
                "file_name": "uploaded_file.pdf",
                "content": open(path, "rb"),
            },
            purpose="ocr"
        )
        self.signed_url = self.mistral_client.files.get_signed_url(file_id=self.uploaded_pdf.id)

    def extract(self):
        """Processes the uploaded PDF and extracts OCR data.

        Returns:
            dict: The OCR response parsed from JSON.
        """
        response = self.mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": self.signed_url.url,
            },
            include_image_base64=True
        )
        return json.loads(response.model_dump_json())

    def get_markdown(self, ocr_response) -> str:
        """Generates Markdown text and gathers image data from the OCR response.

        Iterates over the pages in the OCR response, collecting Markdown text and
        image data (base64 encoded) for each image.

        Args:
            ocr_response (dict): The OCR response containing pages and images.

        Returns:
            tuple: A tuple containing:
                - str: The concatenated Markdown text from all pages.
                - dict: A dictionary mapping image IDs to their base64 encoded image data.
        """
        markdowns: list[str] = []
        image_data = {}
        for page in ocr_response['pages']:
            for img in page['images']:
                image_data[img['id']] = img['image_base64']
            markdowns.append(page['markdown'])
        return "\n\n".join(markdowns), image_data

    def convert_pdf_to_markdown(self, path: str) -> str:
        """Converts a PDF file to Markdown using OCR.

        This high-level method orchestrates the upload, extraction, and conversion
        processes, printing status messages during the process.

        Args:
            path (str): The file path of the PDF to be converted.

        Returns:
            str: The Markdown text extracted from the PDF.
        """
        self.upload(path)
        ocr_response = self.extract()
        self.markdown, self.image_data = self.get_markdown(ocr_response)
        return self.markdown

    def _replace_images_in_markdown(self, markdown_str: str, images_dict: dict) -> str:
        """Replaces image placeholders in Markdown with actual base64 encoded image data.

        Args:
            markdown_str (str): The Markdown text containing image placeholders.
            images_dict (dict): A dictionary mapping image names to base64 encoded strings.

        Returns:
            str: The Markdown text with images replaced by base64 data.
        """
        for img_name, base64_str in images_dict.items():
            markdown_str = markdown_str.replace(f"![{img_name}]({img_name})", f"![{img_name}]({base64_str})")
        return markdown_str


    ###### GPT-4o methods ######
    def generate(self) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": self._get_prompt_for_extractive_query(self.markdown)}
            ],
            temperature=0.
        )
        return response.choices[0].message.content

    def _get_prompt_for_extractive_query(self, markdown: str) -> str:
        return f"""
```
{markdown}
```

Given the markdown string above, your task is to write a list of 10 factoid questions and their answers.
Your factoid questions MUST be answerable with a specific, concise piece of factual information from the texts.
Your factoid questions MUST be formulated in the same style as questions users could ask in a search engine.
This means that your extractive questions MUST NOT mention something like "according to the passage" or "context".
Your factoid questions MUST NOT be about the tables or images in the markdown.
Your factoid questions MUST NOT be about the authors, publication date, references, or any other meta-information.

Provide your answer as follows:

Output:::
Question 1: (your factoid question)
Answer: (your answer to the factoid question)
Question 2: (your factoid question)
Answer: (your answer to the factoid question)
...
Question 10: (your factoid question)
Answer: (your answer to the factoid question)

Now, provide your factoid questions and answers based on the text in the attached file.
Output:::
"""