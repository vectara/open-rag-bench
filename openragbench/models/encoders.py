import os
import gc
import torch
import numpy as np
from tqdm import tqdm
from openai import OpenAI
from google import genai
from google.genai.types import EmbedContentConfig
from sentence_transformers import SentenceTransformer
from tenacity import retry, stop_after_attempt, wait_random_exponential


def similarity_gpu(query_embeddings, doc_embeddings):
    if isinstance(query_embeddings, list):
        query_embeddings = np.array(query_embeddings)
    if isinstance(doc_embeddings, list):
        doc_embeddings = np.array(doc_embeddings)

    assert query_embeddings.shape[1] == doc_embeddings.shape[
        1], "Query and document embeddings must have the same dimension"
    assert query_embeddings.ndim == 2, "Query embeddings should be a 2D array"
    assert doc_embeddings.ndim == 2, "Document embeddings should be a 2D array"

    # Convert to PyTorch tensors and move to GPU
    query_tensor = torch.from_numpy(query_embeddings).cuda()
    doc_tensor = torch.from_numpy(doc_embeddings).cuda()

    # Perform matrix multiplication on GPU
    sim_tensor = torch.matmul(query_tensor, doc_tensor.T)

    # Convert back to numpy for the rest of the processing
    sim_matrix = sim_tensor.cpu().numpy()

    # Apply min-max scaling row-wise (for each query)
    def min_max_scale(x):
        # Find min and max for each row
        min_vals = np.min(x, axis=1, keepdims=True)
        max_vals = np.max(x, axis=1, keepdims=True)

        # Handle the case where min equals max (avoid division by zero)
        range_vals = max_vals - min_vals
        # Where range is 0, set it to 1 to avoid division by zero
        range_vals = np.where(range_vals == 0, 1, range_vals)

        # Apply min-max scaling
        return (x - min_vals) / range_vals

    scaled_matrix = min_max_scale(sim_matrix)

    return scaled_matrix  #.tolist()


def similarity(query_embeddings, doc_embeddings):
    if isinstance(query_embeddings, list):
        query_embeddings = np.array(query_embeddings)
    if isinstance(doc_embeddings, list):
        doc_embeddings = np.array(doc_embeddings)

    assert query_embeddings.shape[1] == doc_embeddings.shape[
        1], "Query and document embeddings must have the same dimension"
    assert query_embeddings.ndim == 2, "Query embeddings should be a 2D array"
    assert doc_embeddings.ndim == 2, "Document embeddings should be a 2D array"

    sim_matrix = query_embeddings @ doc_embeddings.T

    # Apply min-max scaling row-wise (for each query)
    def min_max_scale(x):
        # Find min and max for each row
        min_vals = np.min(x, axis=1, keepdims=True)
        max_vals = np.max(x, axis=1, keepdims=True)

        # Handle the case where min equals max (avoid division by zero)
        range_vals = max_vals - min_vals
        # Where range is 0, set it to 1 to avoid division by zero
        range_vals = np.where(range_vals == 0, 1, range_vals)

        # Apply min-max scaling
        return (x - min_vals) / range_vals

    scaled_matrix = min_max_scale(sim_matrix)

    return scaled_matrix.tolist()


class HuggingfaceEncoder:

    def __init__(self,
                 model_name: str = "",
                 trust_remote_code: bool = False,
                 batch_size: int = 16):
        self.model = SentenceTransformer(model_name,
                                         trust_remote_code=trust_remote_code)
        self.prompt = None
        self.prompt_name = None
        self.batch_size = batch_size

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]
        if self.prompt:
            return self.model.encode(queries,
                                     prompt=self.prompt,
                                     batch_size=self.batch_size,
                                     show_progress_bar=True)
        if self.prompt_name:
            return self.model.encode(queries,
                                     prompt_name=self.prompt_name,
                                     batch_size=self.batch_size,
                                     show_progress_bar=True)

    def encode_docs(self, docs):
        if isinstance(docs, str):
            docs = [docs]
        return self.model.encode(docs,
                                 batch_size=self.batch_size,
                                 show_progress_bar=True)


class LinqEncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "Linq-AI-Research/Linq-Embed-Mistral",
                 batch_size: int = 16):
        super().__init__(model_name, batch_size)
        self.prompt = f"Instruct: Given a question, retrieve passages that answer the question\nQuery: "
        self.model.max_seq_length = 2048


class StellaEncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "dunzhang/stella_en_1.5B_v5",
                 trust_remote_code: bool = True,
                 batch_size: int = 16):
        super().__init__(model_name, trust_remote_code, batch_size)
        self.prompt_name = "s2p_query"


class QwenEncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "Alibaba-NLP/gte-Qwen2-7B-instruct",
                 trust_remote_code: bool = True,
                 batch_size: int = 16):
        super().__init__(model_name, trust_remote_code, batch_size)
        self.prompt_name = "query"
        self.model.max_seq_length = 2048


class JinaEncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "jinaai/jina-embeddings-v3",
                 trust_remote_code: bool = True,
                 batch_size: int = 16):
        super().__init__(model_name, trust_remote_code, batch_size)
        self.prompt_name = "retrieval.query"

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]
        return self.model.encode(queries,
                                 prompt_name=self.prompt_name,
                                 task=self.prompt_name,
                                 batch_size=self.batch_size,
                                 show_progress_bar=True)


class InfEncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "infly/inf-retriever-v1",
                 trust_remote_code: bool = True,
                 batch_size: int = 16):
        super().__init__(model_name, trust_remote_code, batch_size)
        self.prompt_name = "query"
        self.model.max_seq_length = 2048


class SFREncoder(HuggingfaceEncoder):

    def __init__(self,
                 model_name: str = "Salesforce/SFR-Embedding-Mistral",
                 trust_remote_code: bool = True,
                 batch_size: int = 16):
        super().__init__(model_name, trust_remote_code, batch_size)
        self.model.max_seq_length = 2048

    @staticmethod
    def _get_detailed_instruct(query: str) -> str:
        return f'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery: {query}'

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]
        queries = [self._get_detailed_instruct(query) for query in queries]
        return self.model.encode(queries,
                                 batch_size=self.batch_size,
                                 show_progress_bar=True)


class OpenAIEncoder():

    def __init__(self,
                 model_name: str = "text-embedding-3-large",
                 batch_size: int = 16):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model_name
        self.batch_size = batch_size
        self.max_retries = 3  # For handling token limit errors

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def _process_in_batches(self,
                            texts,
                            retry_count=0,
                            current_batch_size=None):
        """Process texts in batches with adaptive batch sizing for token limits"""
        if current_batch_size is None:
            current_batch_size = self.batch_size

        all_embeddings = []

        for i in tqdm(range(0, len(texts), current_batch_size)):
            batch = texts[i:i + current_batch_size]
            try:
                response = self.client.embeddings.create(model=self.model,
                                                         input=batch)
                all_embeddings.extend(
                    [sample.embedding for sample in response.data])
            except Exception as e:
                if "token" in str(e).lower() and retry_count < self.max_retries:
                    new_batch_size = max(1, current_batch_size // 2)
                    print(
                        f"Token limit likely exceeded. Reducing batch size to {new_batch_size} and retrying..."
                    )

                    chunk_embeddings = self._process_in_batches(
                        [item[:8000] for item in batch], retry_count + 1,
                        new_batch_size)
                    all_embeddings.extend(chunk_embeddings)
                else:
                    raise e

        return all_embeddings

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]

        all_embeddings = self._process_in_batches(queries)
        return np.array(all_embeddings)

    def encode_docs(self, docs):
        if isinstance(docs, str):
            docs = [docs]

        all_embeddings = self._process_in_batches(docs)
        return np.array(all_embeddings)


###### DEPRECATED ######
class NVEncoder(HuggingfaceEncoder):
    """THIS CLASS IS NOT WORKING PROPERLY DOE TO POSITION_EMBEDDINGS == NONE"""

    def __init__(self,
                 model_name: str = "nvidia/NV-Embed-v2",
                 trust_remote_code: bool = True):
        super().__init__(model_name, trust_remote_code)
        self.prompt = "Instruct: Given a question, retrieve passages that answer the question\nQuery: "
        self.batch_size = 2
        self.model.max_seq_length = 32768
        self.model.tokenizer.padding_side = "right"

    def add_eos(self, input_examples):
        input_examples = [
            input_example + self.model.tokenizer.eos_token
            for input_example in input_examples
        ]
        return input_examples

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]
        queries = self.add_eos(queries)
        return self.model.encode(queries,
                                 batch_size=self.batch_size,
                                 prompt=self.prompt,
                                 normalize_embeddings=True)

    def encode_docs(self, docs):
        if isinstance(docs, str):
            docs = [docs]
        docs = self.add_eos(docs)
        return self.model.encode(docs,
                                 batch_size=self.batch_size,
                                 normalize_embeddings=True)


class GeminiEncoder():

    def __init__(self,
                 model_name: str = "gemini-embedding-exp-03-07",
                 batch_size: int = 16):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model = model_name
        self.batch_size = batch_size  # Default to max API batch size

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def get_embs(self, texts, task_type):
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=EmbedContentConfig(task_type=task_type,
                                      output_dimensionality=768),
        )
        return [embedding.values for embedding in response.embeddings]

    def encode_queries(self, queries):
        if isinstance(queries, str):
            queries = [queries]

        all_embeddings = []

        for i in tqdm(range(0, len(queries), self.batch_size)):
            batch = queries[i:i + self.batch_size]
            embeddings = self.get_embs(batch, "RETRIEVAL_QUERY")
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)

    def encode_docs(self, docs):
        if isinstance(docs, str):
            docs = [docs]

        all_embeddings = []

        for i in tqdm(range(0, len(docs), self.batch_size)):
            batch = docs[i:i + self.batch_size]
            embeddings = self.get_embs(batch, "RETRIEVAL_DOCUMENT")
            all_embeddings.extend(embeddings)

        return np.array(all_embeddings)


if __name__ == "__main__":
    # Sample data
    queries = [
        'How to bake a chocolate cake',
        'Symptoms of the flu',
        "What are some ways to reduce stress?",
        "What are the benefits of drinking green tea?",
    ]

    passages = [
        "To bake a delicious chocolate cake, you'll need the following ingredients: all-purpose flour, sugar, cocoa powder, baking powder, baking soda, salt, eggs, milk, vegetable oil, and vanilla extract. Start by preheating your oven to 350°F (175°C). In a mixing bowl, combine the dry ingredients (flour, sugar, cocoa powder, baking powder, baking soda, and salt). In a separate bowl, whisk together the wet ingredients (eggs, milk, vegetable oil, and vanilla extract). Gradually add the wet mixture to the dry ingredients, stirring until well combined. Pour the batter into a greased cake pan and bake for 30-35 minutes. Let it cool before frosting with your favorite chocolate frosting. Enjoy your homemade chocolate cake!",
        "The flu, or influenza, is an illness caused by influenza viruses. Common symptoms of the flu include a high fever, chills, cough, sore throat, runny or stuffy nose, body aches, headache, fatigue, and sometimes nausea and vomiting. These symptoms can come on suddenly and are usually more severe than the common cold. It's important to get plenty of rest, stay hydrated, and consult a healthcare professional if you suspect you have the flu. In some cases, antiviral medications can help alleviate symptoms and reduce the duration of the illness.",
        "There are many effective ways to reduce stress. Some common techniques include deep breathing, meditation, and physical activity. Engaging in hobbies, spending time in nature, and connecting with loved ones can also help alleviate stress. Additionally, setting boundaries, practicing self-care, and learning to say no can prevent stress from building up.",
        "Green tea has been consumed for centuries and is known for its potential health benefits. It contains antioxidants that may help protect the body against damage caused by free radicals. Regular consumption of green tea has been associated with improved heart health, enhanced cognitive function, and a reduced risk of certain types of cancer. The polyphenols in green tea may also have anti-inflammatory and weight loss properties.",
    ]

    def clear_memory():
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # List of encoder classes to test
    encoder_classes = [{
        "class": LinqEncoder,
        "name": "LinqEncoder",
        "api_required": False
    }, {
        "class": StellaEncoder,
        "name": "StellaEncoder",
        "api_required": False
    }, {
        "class": QwenEncoder,
        "name": "QwenEncoder",
        "api_required": False
    }, {
        "class": JinaEncoder,
        "name": "JinaEncoder",
        "api_required": False
    }, {
        "class": InfEncoder,
        "name": "InfEncoder",
        "api_required": False
    }, {
        "class": SFREncoder,
        "name": "SFREncoder",
        "api_required": False
    }, {
        "class": GeminiEncoder,
        "name": "GeminiEncoder",
        "api_required": True,
        "api_key": "GEMINI_API_KEY"
    }, {
        "class": OpenAIEncoder,
        "name": "OpenAIEncoder",
        "api_required": True,
        "api_key": "OPENAI_API_KEY"
    }]

    # Run tests for each encoder
    for encoder_info in encoder_classes:
        # Skip API-based encoders if the API key is not available
        if encoder_info["api_required"] and encoder_info[
                "api_key"] not in os.environ:
            print(
                f"\nSkipping {encoder_info['name']} test as {encoder_info['api_key']} environment variable is not set"
            )
            continue

        print(f"\n=== Testing {encoder_info['name']} ===")
        try:
            encoder = encoder_info["class"]()
            query_embeddings = encoder.encode_queries(queries)
            passage_embeddings = encoder.encode_docs(passages)
            similarities = similarity(query_embeddings, passage_embeddings)

            print("Top matching passages for each query:")
            for i, query in enumerate(queries):
                print(f"\nQuery: {query}")
                best_match_idx = similarities[i].index(max(similarities[i]))
                print(
                    f"Best match (score: {similarities[i][best_match_idx]:.4f}): {passages[best_match_idx][:100]}..."
                )
        except Exception as e:
            print(f"Error testing {encoder_info['name']}: {str(e)}")
        finally:
            # Clean up memory
            del encoder, query_embeddings, passage_embeddings, similarities
            clear_memory()
