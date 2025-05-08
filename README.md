# Open RAG Benchmark
A multimodal Retrieval-Augmented Generation (RAG) dataset built from PDF documents.

## Overview
This project delivers high-quality, multimodal datasets for training and evaluating RAG systems. The current implementation focuses on PDF documents, with special attention to preserving text, tables, and images alongside relevant retrieval queries.

Our dataset aims to provide:
- Comprehensive multimodal content from various document types
- High-quality retrieval queries paired with appropriate answers
- Content that spans multiple domains and knowledge areas
- Support for evaluating RAG systems' handling of multimodal information

## Current Progress
We have finalized a draft version of our Arxiv dataset as the first step in our multimodal RAG dataset collection:
- Documents: **1000 PDF papers** evenly distributed across all Arxiv categories.
	- 400 positive documents (i.e., each one is the golden document for some queries)
	- 600 hard negative documents (i.e., they are completely irrelevant to all queries)
- Multimodal Content: Extracted text, tables, and images from research papers
- QA Pairs: 3045 valid question-answer pairs.
	- Based on query types:
		- 1793 abstractive queries (i.e., queries that require generating a summary or rephrased response using understanding and synthesis)
		- 1252 extractive queries (i.e., queries that seek concise, fact-based answer directly extracted from a given text)
	- Based on generation sources:
		- 1914 text-only queries
		- 763 text-image queries
		- 148 text-table queries
		- 220 text-table-image queries

## Repository Structure
This repository contains the code used to generate and refine our dataset:

```
├── configs/                           # Configuration files
│   ├── arxiv_configs.yaml             # Arxiv-specific configuration
│   └── query_configs.yaml             # Query generation/evaluation configuration
├── pipeline/                      # Workflow pipelines
│   ├── data_processing/           # Data processing scripts
│   │   ├── get_arxiv.py           # Script to download Arxiv papers
│   │   ├── parse_arxiv.py         # Script to parse Arxiv PDFs
│   │   ├── get_embeddings.py      # Script for generating embeddings
│   │   └── mine_hns.py            # Script for mining hard-negative samples
│   ├── query_generation/          # Query generation scripts
│   │   ├── generate_qa_pairs.py   # Main script for generating QA pairs
│   │   └── concat_sections_with_metadata.py # Script to concat sections with metadata
│   └── post_filtering/            # Post-processing scripts
│       ├── delete_invalid_queries.py # Script for deleting invalid queries
│       ├── filter_by_doc_relevance.py # Script for filtering by relevance
│       ├── validate_query_type.py # Script for validating query types
│       └── convert_processed_to_dataset.py # Convert processed data to deliverable dataset
├── models/                            # Core processing modules
│   ├── encoders.py                    # Embedding model modules
│   ├── processors.py                  # Document processing utilities
│   ├── query_generator.py             # Query generation logic
│   └── query_evaluator.py             # Query evaluation/filtering logic
├── prompts/                           # LLM prompts
│   └── arxiv_templates.py             # Arxiv-specific prompt templates
└── utils.py                           # Utility functions
```

## Dataset Format
Our dataset resembles the [BEIR dataset](https://github.com/beir-cellar/beir) format.

- `pdf_urls.json`: This file provides the original PDF links to the papers in this dataset for downloading purpose, in the format below:
```
{
	"Paper ID": "Paper URL",
	...
}
```

- `corpus/`: This folder contains all papers processed in the JSON format below:
```
{
	"title": "Paper Title",
	"sections": [
		{
			"text": "Section text content with placeholders for tables/images",
			"tables": {"table_id1": "markdown_table_string", ...},
			"images": {"image_id1": "base64_encoded_string", ...},
		},
		...
	],
	"id": "Paper ID",
	"authors": ["Author1", "Author2", ...],
	"categories: ["Category1", "Category2", ...],
	"abstract": "Abstract text",
	"updated": "Updated date",
	"published": "Published date"
}
```

- `queries.json`: This file contains all generated queries in the format below:
```
{
	"Query UUID": {
		"query": "Query text",
		"type": "Query type (abstractive/extractive)",
		"source": "Generation source (text/text-image/text-table/text-table-image)"
	},
	...
}
```

- `qrels.json`: This file contains the query-document-section relevance labels in the format below:
```
{
	"Query UUID": {
		"doc_id": "Paper ID",
		"section_id": Section Index
	},
	...
}
```

- `answers.json`: This file contains the answers for the generated queries in the format below:
```
{
	"Query UUID": "Answer text",
	...
}
```

## Dataset Generation Process
Our dataset is created through a systematic process:
- Document Collection: Gathering documents from sources like Arxiv.
- Document Processing: Parsing PDFs via OCR into text, Markdown tables, and base64 encoded images.
- Content Segmentation: Dividing documents into sections based on structural elements.
- Query Generation: Using LLMs (currently `gpt-4o-mini`) to generate retrieval queries for each section.
- Quality Filtering: Removing non-retrieval queries and ensuring quality through post-processing via a set of encoders for retrieval filtering and `gpt-4o-mini` for query quality filtering.

## Replication
### Setup
1. Clone this repository:

    ```bash
    git clone [repository-url]
    cd Open-RAG-Benchmark
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install Flash Attention:

    ```bash
    pip install flash-attn --no-build-isolation
    ```

4. Configure your OpenAI API key:

    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

### Workflow

The workflow for generating an Arxiv RAG dataset now consists of four main stages: Data Processing, Query Generation, Post-Filtering of Queries, and Mining Hard-Negative Documents. Below is a detailed breakdown of each stage:

#### 1. Data Processing

This initial stage focuses on downloading and processing raw documents from Arxiv.

1.1. **Download Raw PDFs**

Execute the following script to download PDFs based on configurations defined in `configs/arxiv_configs.yaml`:

```bash
python openragbench/pipeline/data_processing/get_arxiv.py
```

1.2. **Parse PDFs to Structured Format**

Use this script to process PDFs using OCR, extract text, tables, and images, and store the results in a structured JSON format:

```bash
python openragbench/pipeline/data_processing/parse_arxiv.py
```

#### 2. Query Generation

In this stage, queries are generated and enriched with metadata for retrieval purposes.

2.1. **Generate QA Pairs**

Segment documents into sections and generate retrieval queries for each section using LLMs, handling multimodal content such as tables and images:

```bash
python openragbench/pipeline/query_generation/generate_qa_pairs.py
```

2.2. **Concatenate Sections with Metadata**

Combine the generated queries with document metadata for context:

```bash
python openragbench/pipeline/query_generation/concat_sections_with_metadata.py
```

#### 3. Post-Filtering of Queries

This stage aims to enhance the quality of the generated queries.

3.1. **Delete Invalid Queries**

Remove queries that are invalid or poorly styled:

```bash
python openragbench/pipeline/post_filtering/delete_invalid_queries.py
```

3.2. **Filter and Deduplicate**

Execute the following scripts to filter queries based on document relevance, remove duplicates, balance them, and ensure they do not exceed the maximum threshold per document:

```bash
# Get embeddings for filtering
python openragbench/pipeline/data_processing/get_embeddings.py

# Filter queries
python openragbench/pipeline/post_filtering/filter_by_doc_relevance.py
```

3.3. **Validate Query Types**

Ensure all query types are validated and error-free with the following script:

```bash
python openragbench/pipeline/post_filtering/validate_query_type.py
```

3.4. **Convert to Final Dataset**

Translate all processed data into a final, deliverable dataset:

```bash
python openragbench/pipeline/post_filtering/convert_processed_to_dataset.py
```

#### 4. Mining Hard-Negative Documents (Optional)

This optional step involves mining hard negative documents that are entirely irrelevant to any existing query. It relies on agreement across multiple embedding models for accuracy. Specific customizations can be referenced in the script:

```bash
python openragbench/pipeline/data_processing/mine_hns.py
```

## Current Challenges
Several challenges in our dataset development process include:
- **OCR Performance**:
  - Mistral OCR performs well for structured documents but struggles with unstructured PDFs
- **Multimodal Integration**:
  - Ensuring proper extraction and integration of tables and images remains challenging

## Next Steps
### Enhanced Dataset Structure and Usability:
- **Dataset Format and Content Enhancements**
  - Rich Metadata: Add comprehensive document metadata (authors, publication date, categories, etc.) to enable better filtering and contextualization
  - Flexible Chunking: Provide multiple content granularity levels (sections, paragraphs, sentences) to accommodate different retrieval strategies
  - Query Metadata: Classify queries by type (factual, conceptual, analytical), difficulty level, and whether they require multimodal understanding
- **Advanced Multimodal Representation**
  - Improved Image Integration: Replace basic placeholders with structured image objects including captions, alt text, and direct access URLs
  - Structured Table Format: Provide both markdown and programmatically accessible structured formats for tables (headers/rows)
  - Positional Context: Maintain clear positional relationships between text and visual elements
- **Sophisticated Query Generation**
  - Multi-stage Generation Pipeline: Implement targeted generation for different query types (factual, conceptual, multimodal)
  - Diversity Controls: Ensure coverage of different difficulty levels and reasoning requirements
  - Specialized Multimodal Queries: Generate queries specifically designed to test table and image understanding
- **Practitioner-Focused Tools**
  - Framework Integration Examples: Provide code samples showing dataset integration with popular RAG frameworks (LangChain, LlamaIndex, etc.)
  - Evaluation Utilities: Develop standardized tools to benchmark RAG system performance using our dataset
  - Interactive Explorer: Create a simple visualization tool to browse and understand dataset contents

### Dataset Expansion
- Implement alternative solutions for PDF table & image extraction
- Enhance OCR capabilities for unstructured documents
- Broaden scope beyond academic papers to include other document types
- Potentially add multilingual support

## Acknowledgments
We use OpenAI's GPT models for query generation and evaluation. We used the following models for post-filtering for their outstanding performance on the [MTEB Benchmark](https://huggingface.co/spaces/mteb/leaderboard):
- [Linq-AI-Research/Linq-Embed-Mistral](https://huggingface.co/Linq-AI-Research/Linq-Embed-Mistral)
- [dunzhang/stella_en_1.5B_v5](https://huggingface.co/NovaSearch/stella_en_1.5B_v5)
- [Alibaba-NLP/gte-Qwen2-7B-instruct](https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct)
- [infly/inf-retriever-v1](https://huggingface.co/infly/inf-retriever-v1)
- [Salesforce/SFR-Embedding-Mistral](https://huggingface.co/Salesforce/SFR-Embedding-Mistral)
- [openai/text-embedding-3-large](https://platform.openai.com/docs/models/text-embedding-3-large)