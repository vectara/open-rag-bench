import os
from typing import Any, Dict, List, Optional
from openai import OpenAI
from openai.types import FileObject
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run
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