import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

from utils import read_config
from openai import OpenAI
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential
from prompts.arxiv_templates import POST_FILTERING_INSTRUCTION

PROMPT = POST_FILTERING_INSTRUCTION
OPENAI_MODELS = read_config("query_configs.yaml")["OPENAI_MODELS"]


class QueryEvaluator:

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

    @staticmethod
    def _count_tokens(response):
        return {
            'input': response['usage']['input_tokens'],
            'output': response['usage']['output_tokens'],
        }

    @staticmethod
    def _validate_answer(answer):
        if 'yes' in answer.lower():
            return True
        if 'no' in answer.lower():
            return False
        return None

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def evaluate(self, query) -> bool:
        prompt = PROMPT.format(query=query)
        self.model_args.update(
            {"messages": [{
                "role": "user",
                "content": prompt
            }]})
        answer = None
        failure_counter = 0
        while answer is None and failure_counter < 5:
            response = self.client.chat.completions.create(**self.model_args)
            response_text = response.choices[0].message.content.strip()
            answer = self._validate_answer(response_text)
            failure_counter += 1

        if answer is None:
            raise ValueError(
                "Failed to generate a valid answer after multiple attempts.")
        return answer


if __name__ == "__main__":
    query = "Is the sky blue?"
    evaluator = QueryEvaluator()
    result = evaluator.evaluate(query)
    print(f"Evaluation result for '{query}': {result}")

    query = "Is the sky blue in the context?"
    evaluator = QueryEvaluator()
    result = evaluator.evaluate(query)
    print(f"Evaluation result for '{query}': {result}")
