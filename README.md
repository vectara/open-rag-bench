# Open RAG Benchmark
A multimodal (and potentially multilingual) Retrieval-Augmented Generation (RAG) dataset built from PDF documents.

## Overview
This project delivers high-quality, multimodal datasets for training and evaluating RAG systems. The current implementation focuses on PDF documents, with special attention to preserving text, tables, and images alongside relevant retrieval queries.

Our dataset aims to provide:
- Comprehensive multimodal content from various document types
- High-quality retrieval queries paired with appropriate answers
- Content that spans multiple domains and knowledge areas
- Support for evaluating RAG systems' handling of multimodal information

## Current Progress
We have finalized a draft version of our Arxiv dataset as the first step in our multimodal RAG dataset collection:
- Documents: 400 PDF papers evenly distributed across all Arxiv categories
- QA Pairs: 16,000+ valid question-answer pairs
- Multimodal Content: Extracted text, tables, and images from research papers

## Repository Structure
This repository contains the code used to generate and refine our dataset:

```
├── configs/                    # Configuration files
│   ├── arxiv_configs.yaml      # Arxiv-specific configuration
│   └── query_configs.yaml      # Query generation/evaluation configuration
├── data/                       # Dataset storage
│   ├── ocr/                    # Intermediate OCR results
│   ├── processed/              # Final processed datasets
│   └── raw/                    # Original unmodified data
├── data_processing/            # Dataset-specific processing scripts
│   └── arxiv/                  # Arxiv-specific processing
│       ├── get_arxiv.py        # Script to download Arxiv papers
│       └── parse_arxiv.py      # Script to parse Arxiv PDFs
├── models/                     # Core processing modules
│   ├── processors.py           # Document processing utilities
│   ├── query_generator.py      # Query generation logic
│   └── query_evaluator.py      # Query evaluation/filtering logic
├── prompts/                    # LLM prompts
│   └── arxiv_templates.py      # Arxiv-specific prompt templates
├── generate_qa_pairs.py        # Main script for generating QA pairs
├── post_filtering.py           # Script for filtering generated queries
└── utils.py                    # Utility functions
```

## Dataset Format
Each document in the dataset is represented as a JSON file with the following structure:

```
{
  "title": "Paper Title",
  "sections": [
    {
      "text": "Section text content with placeholders for tables/images",
      "tables": {"table_id1": "markdown_table_string", ...},
      "images": {"image_id1": "base64_encoded_string", ...},
      "qa_pairs": [
        {"query": "Query text", "answer": "Answer text"},
        ...
      ]
    },
    ...
  ]
}
```

## Dataset Generation Process
Our dataset is created through a systematic process:
- Document Collection: Gathering documents from sources like Arxiv
- Document Processing: Parsing PDFs via OCR into text, Markdown tables, and base64 encoded images
- Content Segmentation: Dividing documents into sections based on structural elements
- Query Generation: Using LLMs (currently gpt-4o-mini and gpt-4o) to generate retrieval queries for each section
- Quality Filtering: Removing non-retrieval queries and ensuring quality through post-processing

## Replication
### Setup
1. Clone this repository:

    ```
    git clone [repository-url]
    cd multimodal-rag-dataset
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Configure your OpenAI API key:

    ```
    export OPENAI_API_KEY="your-api-key"
    ```

### Workflow
The complete workflow for generating an Arxiv RAG dataset involves the following steps:
1. Download Raw PDFs

    ```
    python data_processing/arxiv/get_arxiv.py
    ```

    This downloads PDFs from Arxiv based on configurations in configs/arxiv_configs.yaml.

2. Parse PDFs to Structured Format

    ```
    python data_processing/arxiv/parse_arxiv.py
    ```

    This script:
    - Processes the raw PDFs using OCR
    - Extracts text, tables, and images
    - Stores results in JSON format with placeholders for tables and images

3. Generate QA Pairs

    ```
    python generate_qa_pairs.py
    ```

    This script:
    - Segments documents into sections
    - Generates retrieval queries per section using LLMs
    - Handles multimodal content (tables and images)

4. Post-Filter QA Pairs

    ```
    python post_filtering.py
    ```

    This script filters out invalid or low-quality queries.

## Current Challenges
Several challenges in our dataset development process include:
- Query Quality:
    - Many queries remain too specific to individual sections despite filtering
    - Some queries still assume prior document knowledge
- OCR Performance:
    - Mistral OCR performs well for structured documents but struggles with unstructured PDFs
- Multimodal Integration:
    - Ensuring proper extraction and integration of tables and images remains challenging

## Next Steps
### Enhanced Filtering:
- Implement deduplication of similar queries
- Add semantic similarity scoring
- Develop query diversity metrics
- Implement document-based LLM filtering

### Enhanced Dataset Structure and Usability:
- Dataset Format and Content Enhancements
    - Rich Metadata: Add comprehensive document metadata (authors, publication date, categories, citation counts) to enable better filtering and contextualization
    - Flexible Chunking: Provide multiple content granularity levels (sections, paragraphs, sentences) to accommodate different retrieval strategies
    Query Metadata: Classify queries by type (factual, conceptual, analytical), difficulty level, and whether they require multimodal understanding
- Advanced Multimodal Representation
    - Improved Image Integration: Replace basic placeholders with structured image objects including captions, alt text, and direct access URLs
    - Structured Table Format: Provide both markdown and programmatically accessible structured formats for tables (headers/rows)
    - Positional Context: Maintain clear positional relationships between text and visual elements
- Sophisticated Query Generation
    - Multi-stage Generation Pipeline: Implement targeted generation for different query types (factual, conceptual, multimodal)
    - Diversity Controls: Ensure coverage of different difficulty levels and reasoning requirements
    - Specialized Multimodal Queries: Generate queries specifically designed to test table and image understanding
- Practitioner-Focused Tools
    - Framework Integration Examples: Provide code samples showing dataset integration with popular RAG frameworks (LangChain, LlamaIndex, etc.)
    - Evaluation Utilities: Develop standardized tools to benchmark RAG system performance using our dataset
    - Interactive Explorer: Create a simple visualization tool to browse and understand dataset contents

### Dataset Expansion
- Implement alternative solutions for PDF table & image extraction
- Enhance OCR capabilities for unstructured documents
- Broaden scope beyond academic papers to include other document types
- Potentially add multilingual support

## License
(tbd)

## Acknowledgments
We use OpenAI's GPT models for query generation and evaluation. (tbd)
