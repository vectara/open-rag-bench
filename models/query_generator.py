import os
import re

from openai import OpenAI
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential

from prompts.arxiv_templates import *

PROMPT_MAP = {
    "text_extractive": TEXT_EXTRACTIVE_INSTRUCTION,
    "text_abstractive": TEXT_ABSTRACTIVE_INSTRUCTION,
}


class BaseQueryGenerator:
    def __init__(self):
        pass

    @staticmethod
    def _extract_qa_pairs(llm_output: str) -> Optional[List[Dict[str, str]]]:
        """
        Processes the LLM output by:
        1. Splitting the text into lines.
        2. Finding the block from "Question 1:" to "Answer 5:" (discarding any extra lines after).
        3. Parsing that block into exactly 5 QA pairs.

        Each QA pair is returned as a dictionary with keys "query" and "answer".

        If the valid QA block is not found, returns None.
        """
        if not llm_output:
            return None

        # Split the text into lines and remove empty lines
        lines = [line for line in llm_output.splitlines() if line.strip()]

        # Find the start index (first occurrence of "Question 1:")
        try:
            start_idx = next(i for i, line in enumerate(lines) if line.strip().startswith("Question 1:"))
        except StopIteration:
            return None

        # Find the end index (first occurrence of "Answer 5:")
        try:
            end_idx = next(i for i, line in enumerate(lines) if line.strip().startswith("Answer 5:"))
        except StopIteration:
            return None

        # Slice the valid block and join back into a single string
        valid_text = "\n".join(lines[start_idx:end_idx+1])

        # Define a regex pattern that captures the 5 QA pairs from the valid text block.
        pattern = (
            r"Question\s*1:\s*(?P<q1>.+?)\s*"
            r"Answer\s*1:\s*(?P<a1>.+?)\s*"
            r"Question\s*2:\s*(?P<q2>.+?)\s*"
            r"Answer\s*2:\s*(?P<a2>.+?)\s*"
            r"Question\s*3:\s*(?P<q3>.+?)\s*"
            r"Answer\s*3:\s*(?P<a3>.+?)\s*"
            r"Question\s*4:\s*(?P<q4>.+?)\s*"
            r"Answer\s*4:\s*(?P<a4>.+?)\s*"
            r"Question\s*5:\s*(?P<q5>.+?)\s*"
            r"Answer\s*5:\s*(?P<a5>.+)"
        )

        match = re.fullmatch(pattern, valid_text, re.DOTALL)
        if not match:
            return None

        qa_pairs = []
        for i in range(1, 6):
            question = match.group(f"q{i}").strip()
            answer = match.group(f"a{i}").strip()
            qa_pairs.append({"query": question, "answer": answer})

        return qa_pairs

    @staticmethod
    def _header_contains_keywords(markdown_text):
        """
        Checks if any header line in the markdown text contains any of the
        keywords 'introduction', 'abstract', or 'conclusion', regardless of case.

        Only lines that start with one or more '#' characters are considered.

        Args:
            markdown_text (str): The markdown text to check.

        Returns:
            bool: True if a header line contains one of the keywords, False otherwise.
        """
        # Define the regex pattern:
        # ^#+   : the line starts with one or more '#' characters
        # .*    : then any characters
        # \b(...)\b : one of the keywords as a whole word
        pattern = re.compile(r'^#+.*\b(introduction|abstract|conclusion)\b', re.IGNORECASE)

        # Split the text into individual lines and check each header line.
        for line in markdown_text.splitlines():
            if pattern.search(line.strip()):
                return True
        return False


class OpenAIQueryGenerator(BaseQueryGenerator):
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

    def __init__(self, model: str = "gpt-4o-mini", openai_api_key: Optional[str] = None) -> None:
        """Initialize the OpenAI instance."""
        final_openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        if not final_openai_api_key:
            raise ValueError("OpenAI API key is required. Please provide it via function argument or environment variable.")

        self.client: OpenAI = OpenAI(api_key=final_openai_api_key)
        self.model: str = model

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self, title, text, query_type="text") -> str:
        if query_type == "text":
            if self._header_contains_keywords(text):
                query_type = "text_abstractive"
            else:
                query_type = "text_extractive"
        prompt = PROMPT_MAP[query_type].format(title=title, text=text)
        qa_pairs = None
        while qa_pairs is None:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.
            ).choices[0].message.content
            qa_pairs = self._extract_qa_pairs(response)
        return qa_pairs


class VLLMQueryGenerator(BaseQueryGenerator):
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

    def __init__(self, model: str = "Qwen/Qwen2.5-72B-Instruct", vllm_api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        """Initialize the OpenAI instance."""
        final_vllm_api_key = vllm_api_key or os.environ.get("VLLM_API_KEY")
        if not final_vllm_api_key:
            raise ValueError("OpenAI API key is required. Please provide it via function argument or environment variable.")
        final_base_url = base_url or os.environ.get("VLLM_BASE_URL")
        if not final_base_url:
            raise ValueError("Base URL for vLLM is required. Please provide it via function argument.")

        self.client: OpenAI = OpenAI(api_key=final_vllm_api_key, base_url=base_url)
        self.model: str = model

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate(self, title, text, query_type="text") -> str:
        if query_type == "text":
            if self._header_contains_keywords(text):
                query_type = "text_abstractive"
            else:
                query_type = "text_extractive"
        prompt = PROMPT_MAP[query_type].format(title=title, text=text)
        qa_pairs = None
        while qa_pairs is None:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.,
                frequency_penalty=0,
                presence_penalty=0
            ).choices[0].message.content
            qa_pairs = self._extract_qa_pairs(response)
        return qa_pairs