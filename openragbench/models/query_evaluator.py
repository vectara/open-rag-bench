import os
import gc
import torch
import numpy as np
from utils import read_config, read_json, write_json
from openai import OpenAI
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential

from openragbench.prompts.arxiv_templates import STYLE_VALIDATION_INSTRUCTION, TYPE_VALIDATION_INSTRUCTION
from openragbench.models.processors import MarkdownProcessor

OPENAI_MODELS = read_config("query_configs.yaml")["OPENAI_MODELS"]


class StyleValidator:

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
        prompt = STYLE_VALIDATION_INSTRUCTION.format(query=query)
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


class DocumentRelevanceFilter:

    def __init__(self):
        from models.encoders import (LinqEncoder, StellaEncoder, QwenEncoder,
                                     JinaEncoder, InfEncoder, SFREncoder,
                                     GeminiEncoder, OpenAIEncoder, similarity)
        self.encoder_classes = [
            {
                "class": LinqEncoder,
                "name": "LinqEncoder",
                "api_required": False
            },
            {
                "class": StellaEncoder,
                "name": "StellaEncoder",
                "api_required": False
            },
            {
                "class": QwenEncoder,
                "name": "QwenEncoder",
                "api_required": False
            },
            # {"class": JinaEncoder, "name": "JinaEncoder", "api_required": False},
            {
                "class": InfEncoder,
                "name": "InfEncoder",
                "api_required": False
            },
            {
                "class": SFREncoder,
                "name": "SFREncoder",
                "api_required": False
            },
            # {"class": GeminiEncoder, "name": "GeminiEncoder", "api_required": True, "api_key": "GEMINI_API_KEY"},
            {
                "class": OpenAIEncoder,
                "name": "OpenAIEncoder",
                "api_required": True,
                "api_key": "OPENAI_API_KEY"
            }
        ]
        self.similarity = similarity

    @staticmethod
    def clear_memory():
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def compute_similarity(self, embeddings1, embeddings2):
        return self.similarity(embeddings1, embeddings2)

    def compute_query_embeddings(self, query_path, output_dir):
        queries = read_json(query_path)
        query_items = sorted(queries.items())
        query_texts = [item[1]['query'] for item in query_items]
        query_id_to_index = {
            query_id: idx for idx, (query_id, _) in enumerate(query_items)
        }

        os.makedirs(output_dir, exist_ok=True)

        for encoder_info in self.encoder_classes:
            # Skip API-based encoders if the API key is not available
            if encoder_info["api_required"] and encoder_info[
                    "api_key"] not in os.environ:
                print(
                    f"\nSkipping {encoder_info['name']} test as {encoder_info['api_key']} environment variable is not set"
                )
                continue

            print(f"Encoding queries with {encoder_info['name']}")
            try:
                subfolder_path = os.path.join(output_dir, encoder_info["name"])
                os.makedirs(subfolder_path, exist_ok=True)
                if os.path.exists(
                        os.path.join(subfolder_path, "query_embeddings.npy")):
                    print(
                        f"Query embeddings for {encoder_info['name']} already exist. Skipping computation."
                    )
                    continue

                encoder = encoder_info["class"]()
                query_embeddings = encoder.encode_queries(query_texts)

                np.save(os.path.join(subfolder_path, "query_embeddings.npy"),
                        query_embeddings)
            except Exception as e:
                print(f"Error testing {encoder_info['name']}: {str(e)}")
            finally:
                if 'encoder' in locals():
                    del encoder
                if 'query_embeddings' in locals():
                    del query_embeddings
                self.clear_memory()

        write_json(query_id_to_index,
                   os.path.join(output_dir, "query_id_to_index.json"))

    def compute_section_embeddings(self, corpus_path, output_dir):
        processor = MarkdownProcessor()
        sections_data = []  # Will hold all section texts
        section_id_to_index = {}  # Three-level nested dictionary for mapping

        # Process all documents and their sections
        section_index = 0
        for filename in sorted(os.listdir(corpus_path)):
            if filename.endswith('.json'):
                doc_id = filename.replace('.json', '')
                data = read_json(os.path.join(corpus_path, filename))

                # Extract title from the data
                title = data.get('title', '')

                # Initialize the document entry in the mapping dictionary
                section_id_to_index[doc_id] = {}

                # Process each section
                for i, section in enumerate(data.get('sections', [])):
                    # Concatenate title and section text with double newline
                    section_text = processor.convert_section_to_chunk_text(
                        section)
                    section_text = f"{title}\n\n{section_text}"
                    sections_data.append(section_text)

                    # Map document ID -> section ID -> embedding index
                    section_id_to_index[doc_id][str(i)] = section_index
                    section_index += 1

        os.makedirs(output_dir, exist_ok=True)

        # Save the mapping dictionary
        write_json(section_id_to_index,
                   os.path.join(output_dir, "section_id_to_index.json"))

        # Process with each encoder
        for encoder_info in self.encoder_classes:
            # Skip API-based encoders if the API key is not available
            if encoder_info["api_required"] and encoder_info[
                    "api_key"] not in os.environ:
                print(
                    f"\nSkipping {encoder_info['name']} test as {encoder_info['api_key']} environment variable is not set"
                )
                continue

            print(f"Encoding sections with {encoder_info['name']}")
            try:
                subfolder_path = os.path.join(output_dir, encoder_info["name"])
                os.makedirs(subfolder_path, exist_ok=True)

                # Skip if embeddings already exist
                if os.path.exists(
                        os.path.join(subfolder_path, "section_embeddings.npy")):
                    print(
                        f"Section embeddings for {encoder_info['name']} already exist. Skipping computation."
                    )
                    continue

                # Create and use the encoder
                encoder = encoder_info["class"]()
                encoder.batch_size = 16
                section_embeddings = encoder.encode_docs(sections_data)

                # Save the embeddings
                np.save(os.path.join(subfolder_path, "section_embeddings.npy"),
                        section_embeddings)
            except Exception as e:
                print(f"Error testing {encoder_info['name']}: {str(e)}")
            finally:
                # Clean up to free memory
                if 'encoder' in locals():
                    del encoder
                if 'section_embeddings' in locals():
                    del section_embeddings
                self.clear_memory()

    def compute_doc_embeddings(self, corpus_path, output_dir):
        processor = MarkdownProcessor()
        docs = {}
        for filename in os.listdir(corpus_path):
            if filename.endswith('.json'):
                data = read_json(os.path.join(corpus_path, filename))
                docs[filename.replace('.json',
                                      '')] = processor.sections_to_doc(data)

        doc_items = sorted(docs.items())
        doc_texts = [item[1] for item in doc_items]
        doc_id_to_index = {
            doc_id: idx for idx, (doc_id, _) in enumerate(doc_items)
        }

        os.makedirs(output_dir, exist_ok=True)

        for encoder_info in self.encoder_classes:
            # Skip API-based encoders if the API key is not available
            if encoder_info["api_required"] and encoder_info[
                    "api_key"] not in os.environ:
                print(
                    f"\nSkipping {encoder_info['name']} test as {encoder_info['api_key']} environment variable is not set"
                )
                continue

            print(f"Encoding docs with {encoder_info['name']}")
            try:
                subfolder_path = os.path.join(output_dir, encoder_info["name"])
                os.makedirs(subfolder_path, exist_ok=True)
                if os.path.exists(
                        os.path.join(subfolder_path, "doc_embeddings.npy")):
                    print(
                        f"Doc embeddings for {encoder_info['name']} already exist. Skipping computation."
                    )
                    continue

                encoder = encoder_info["class"](batch_size=1)
                doc_embeddings = encoder.encode_docs(doc_texts)

                np.save(os.path.join(subfolder_path, "doc_embeddings.npy"),
                        doc_embeddings)
            except Exception as e:
                print(f"Error testing {encoder_info['name']}: {str(e)}")
            finally:
                if 'encoder' in locals():
                    del encoder
                if 'doc_embeddings' in locals():
                    del doc_embeddings
                self.clear_memory()

        write_json(doc_id_to_index,
                   os.path.join(output_dir, "doc_id_to_index.json"))


class TypeValidator:

    def __init__(self,
                 model: str = "gpt-4o",
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
        if 'abstractive' in answer.lower():
            return True
        if 'extractive' in answer.lower():
            return False
        return None

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def evaluate(self, query) -> bool:
        prompt = TYPE_VALIDATION_INSTRUCTION.format(query=query)
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
