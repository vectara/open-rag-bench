import os
import re
from utils import read_config
from openai import OpenAI
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential

from openragbench.models.processors import MarkdownProcessor
from openragbench.prompts.arxiv_templates import PROMPT_MAP, CONTEXT_SUMMARIZATION_INSTRUCTION

OPENAI_MODELS = read_config("query_configs.yaml")["OPENAI_MODELS"]


class QueryGenerator:

    def __init__(self,
                 model: str = "gpt-4o-mini",
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None) -> None:

        if model in OPENAI_MODELS:
            api_key = api_key or os.environ.get("OPENAI_API_KEY")
            base_url = None
        else:
            api_key = api_key or os.environ.get("VLLM_API_KEY")
            base_url = base_url or os.environ.get("VLLM_BASE_URL")
        if not api_key:
            raise ValueError(
                "OpenAI/VLLM API key is required. Please provide it via function argument or environment variable."
            )

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_args = {"model": model}
        if model != "o3-mini":
            self.model_args.update({
                "temperature": 0.,
                "frequency_penalty": 1,
                "seed": 2
            })
        self.processor = MarkdownProcessor()

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def generate_old(self,
                     title,
                     text,
                     table_data=None,
                     image_data=None) -> str:
        if len(text) < 200:
            return []
        if self._header_contains_keywords(text):
            query_type = "abstractive"
        else:
            query_type = "extractive"
        if query_type == "extractive":
            table_instruction, image_instruction = '', ''
            if table_data not in (None, {}):
                table_instruction = TABLE_INSTRUCTION
                text = self.processor.replace_placeholders_in_markdown(
                    text, table_data)
            if image_data not in (None, {}):
                image_instruction = IMAGE_INSTRUCTION
            prompt = PROMPT_MAP[query_type].format(
                title=title,
                text=text,
                table_instruction=table_instruction,
                image_instruction=image_instruction)
        else:
            prompt = PROMPT_MAP[query_type].format(title=title, text=text)

        if image_data not in (None, {}):
            messages = [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": prompt
                }]
            }]
            for base64 in image_data.values():
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": base64,
                        "detail": "high"
                    }
                })
            self.model_args.update({"model": "gpt-4o"})
        else:
            messages = [{"role": "user", "content": prompt}]
        self.model_args.update({"messages": messages})

        qa_pairs = None
        failure_counter = 0
        while qa_pairs is None and failure_counter < 5:
            response = self.client.chat.completions.create(**self.model_args)
            response_text = response.choices[0].message.content
            qa_pairs = self._extract_qa_pairs(response_text)
            failure_counter += 1
        if qa_pairs is None or qa_pairs == []:
            return []
            # raise ValueError("Failed to generate a valid answer after multiple attempts.")
        return qa_pairs

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def generate(self,
                 title,
                 text,
                 table_data=None,
                 image_data=None) -> List[Dict[str, str]]:
        """
        Generate query-answer pairs based on text, tables, and/or images.

        Args:
            title (str): Title of the content
            text (str): Markdown text content
            table_data (Dict, optional): Dictionary of table data
            image_data (Dict, optional): Dictionary of image data as base64 strings

        Returns:
            List[Dict[str, str]]: List of query-answer pairs
        """
        if len(text) < 200:
            return []

        # Case 1: Text only
        if (table_data in (None, {}) and image_data in (None, {})):
            # Determine query type based on header content
            if self._header_contains_keywords(text):
                query_type = "abstractive"
            else:
                query_type = "extractive"
            # return self._generate_text_only(title, text, query_type)
            return []

        # Case 2: Table
        elif table_data not in (None, {}) and image_data in (None, {}):
            qa_pairs = []
            for query_type in ["extractive", "abstractive"]:
                pairs = self._generate_text_table(title, text, table_data,
                                                  query_type)
                qa_pairs.extend(pairs)
            return qa_pairs

        # Case 3: Image
        elif image_data not in (None, {}) and table_data in (None, {}):
            qa_pairs = []
            for query_type in ["extractive", "abstractive"]:
                pairs = self._generate_text_image(title, text, image_data,
                                                  query_type)
                qa_pairs.extend(pairs)
            return qa_pairs

        # Case 4: Text, table, and image (handle each separately and combine results)
        else:
            table_qa_pairs = []
            image_qa_pairs = []

            for query_type in ["extractive", "abstractive"]:
                table_pairs = self._generate_text_table(title, text, table_data,
                                                        query_type)
                image_pairs = self._generate_text_image(title, text, image_data,
                                                        query_type)
                table_qa_pairs.extend(table_pairs)
                image_qa_pairs.extend(image_pairs)

            combined_qa_pairs = table_qa_pairs + image_qa_pairs
            return combined_qa_pairs

    def _generate_text_only(self, title, text, query_type):
        """Generate QA pairs from text only."""
        prompt = PROMPT_MAP["text"][query_type].format(title=title, text=text)

        messages = [{"role": "user", "content": prompt}]
        self.model_args.update({"messages": messages})

        return self._get_qa_pairs_from_llm()

    def _generate_text_table(self, title, text, table_data, query_type):
        """Generate QA pairs from text and table with context summarization."""
        # Step 1: Summarize the context
        context_prompt = CONTEXT_SUMMARIZATION_INSTRUCTION.format(title=title,
                                                                  text=text)

        messages = [{"role": "user", "content": context_prompt}]
        self.model_args.update({"messages": messages})

        response = self.client.chat.completions.create(**self.model_args)
        context = response.choices[0].message.content
        tables = "\n\n".join(table_data.values())

        # Step 2: Generate QA pairs using the context summary and table
        combined_prompt = PROMPT_MAP["text_table"][query_type].format(
            title=title, context=context, table=tables)

        messages = [{"role": "user", "content": combined_prompt}]
        original_model = self.model_args.get("model")
        self.model_args.update({"model": "gpt-4o", "messages": messages})

        qa_pairs = self._get_qa_pairs_from_llm()

        # Restore original model
        self.model_args.update({"model": original_model})

        return qa_pairs

    def _generate_text_image(self, title, text, image_data, query_type):
        """Generate QA pairs from text and image with context summarization."""
        # Step 1: Summarize the context
        context_prompt = CONTEXT_SUMMARIZATION_INSTRUCTION.format(title=title,
                                                                  text=text)

        messages = [{"role": "user", "content": context_prompt}]
        self.model_args.update({"messages": messages})

        response = self.client.chat.completions.create(**self.model_args)
        context = response.choices[0].message.content

        # Step 2: Generate QA pairs using the context summary and image
        text_image_prompt = PROMPT_MAP["text_image"][query_type].format(
            title=title, context=context)

        messages = [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": text_image_prompt
            }]
        }]

        for base64 in image_data.values():
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": base64,
                    "detail": "high"
                }
            })

        original_model = self.model_args.get("model")
        self.model_args.update({"model": "gpt-4o", "messages": messages})

        qa_pairs = self._get_qa_pairs_from_llm()

        # Restore original model
        self.model_args.update({"model": original_model})

        return qa_pairs

    def _generate_table_only(self, title, table_data, query_type):
        """Generate QA pairs from table only."""
        processed_text = self.processor.replace_placeholders_in_markdown(
            "", table_data)
        table_prompt = PROMPT_MAP["table"][query_type].format(
            title=title, text=processed_text)

        messages = [{"role": "user", "content": table_prompt}]
        self.model_args.update({"messages": messages})

        return self._get_qa_pairs_from_llm()

    def _generate_image_only(self, title, image_data, query_type):
        """Generate QA pairs from image only."""
        image_prompt = PROMPT_MAP["image"][query_type].format(title=title)

        messages = [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": image_prompt
            }]
        }]

        for base64 in image_data.values():
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": base64,
                    "detail": "high"
                }
            })

        original_model = self.model_args.get("model")
        self.model_args.update({"model": "gpt-4o", "messages": messages})

        qa_pairs = self._get_qa_pairs_from_llm()

        # Restore original model
        self.model_args.update({"model": original_model})

        return qa_pairs

    def _get_qa_pairs_from_llm(self):
        """Helper method to get QA pairs from LLM with retry logic."""
        qa_pairs = None
        failure_counter = 0
        while qa_pairs is None and failure_counter < 5:
            response = self.client.chat.completions.create(**self.model_args)
            response_text = response.choices[0].message.content
            qa_pairs = self._extract_qa_pairs(response_text)
            failure_counter += 1

        return qa_pairs or []

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

        # Find the start index (first occurrence of "Query 1:")
        try:
            start_idx = next(i for i, line in enumerate(lines)
                             if line.strip().startswith("Query 1:"))
        except StopIteration:
            return None

        # Find the end index (first occurrence of "Answer 5:")
        try:
            end_idx = next(i for i, line in enumerate(lines)
                           if line.strip().startswith("Answer 5:"))
        except StopIteration:
            return None

        # Slice the valid block and join back into a single string
        valid_text = "\n".join(lines[start_idx:end_idx + 1])

        # Define a regex pattern that captures the 5 QA pairs from the valid text block.
        pattern = (r"Query\s*1:\s*(?P<q1>.+?)\s*"
                   r"Answer\s*1:\s*(?P<a1>.+?)\s*"
                   r"Query\s*2:\s*(?P<q2>.+?)\s*"
                   r"Answer\s*2:\s*(?P<a2>.+?)\s*"
                   r"Query\s*3:\s*(?P<q3>.+?)\s*"
                   r"Answer\s*3:\s*(?P<a3>.+?)\s*"
                   r"Query\s*4:\s*(?P<q4>.+?)\s*"
                   r"Answer\s*4:\s*(?P<a4>.+?)\s*"
                   r"Query\s*5:\s*(?P<q5>.+?)\s*"
                   r"Answer\s*5:\s*(?P<a5>.+)")

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
        pattern = re.compile(r'^#+.*\b(introduction|abstract|conclusion)\b',
                             re.IGNORECASE)

        # Split the text into individual lines and check each header line.
        for line in markdown_text.splitlines():
            if pattern.search(line.strip()):
                return True
        return False

    @staticmethod
    def _count_tokens(response):
        return {
            'input': response['usage']['input_tokens'],
            'output': response['usage']['output_tokens'],
        }


if __name__ == "__main__":
    # Example usage
    query_gen = QueryGenerator(model="gpt-4o-mini")
    title = "Sample Title"
    text = "# Introduction\nThis is a sample introduction.\n# Conclusion\nThis is a sample conclusion."
    query_type = "text_extractive"

    try:
        result = query_gen.generate(title, text, query_type)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
