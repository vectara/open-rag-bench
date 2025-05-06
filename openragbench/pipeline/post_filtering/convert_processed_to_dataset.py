import json
import uuid
import re
import argparse
from pathlib import Path


def convert_to_dataset(input_dir, output_dir):
    """
    Process JSON documents to create the required datasets.
    
    Args:
        input_dir: Directory containing the original JSON documents
        output_dir: Directory to save the processed outputs
    """
    # Create output directory structure
    output_path = Path(output_dir)
    corpus_path = output_path / "corpus"
    corpus_path.mkdir(parents=True, exist_ok=True)

    # Initialize dictionaries to collect data
    queries = {}
    answers = {}
    qrels = {}

    # Process each document
    for file_path in Path(input_dir).glob("*.json"):
        # Extract document ID from filename
        doc_id = file_path.stem

        # Load the document
        with open(file_path, 'r', encoding='utf-8') as f:
            document = json.load(f)

        # Make a copy for processing
        processed_doc = document.copy()

        # Process each section
        for section_idx, section in enumerate(document.get('sections', [])):
            # Add section_id to processed document
            processed_section = {
                'section_id': section_idx,
                'text': section.get('text', ''),
                'tables': section.get('tables', {}),
                'images': section.get('images', {})
            }

            # Process QA pairs if they exist
            if 'qa_pairs' in section:
                section_text = section.get('text', '')
                tables = section.get('tables', {})
                images = section.get('images', {})

                # Determine the query type
                section_header_match = re.search(r'####\s+(.*?)[\n\r]',
                                                 section_text)
                query_type = "extractive"
                if section_header_match:
                    header = section_header_match.group(1).lower()
                    if any(keyword in header for keyword in
                           ["abstract", "introduction", "conclusion"]):
                        query_type = "abstractive"

                # Determine the source
                if tables and images:
                    source = "text-table-image"
                elif tables:
                    source = "text-table"
                elif images:
                    source = "text-image"
                else:
                    source = "text"

                for qa_pair in section['qa_pairs']:
                    # Generate a unique ID for this query
                    query_id = str(uuid.uuid4())

                    # Store query with its metadata
                    queries[query_id] = {
                        "query": qa_pair['query'],
                        "type": query_type,
                        "source": source
                    }

                    # Store answer
                    answers[query_id] = qa_pair['answer']

                    # Store document and section reference
                    qrels[query_id] = {
                        'doc_id': doc_id,
                        'section_id': section_idx
                    }

            # Update the processed document with the modified section
            processed_doc['sections'][section_idx] = processed_section

        # Save the processed document
        with open(corpus_path / f"{doc_id}.json", 'w', encoding='utf-8') as f:
            json.dump(processed_doc, f)

    # Save the generated datasets
    with open(output_path / "queries.json", 'w', encoding='utf-8') as f:
        json.dump(queries, f)

    with open(output_path / "answers.json", 'w', encoding='utf-8') as f:
        json.dump(answers, f)

    with open(output_path / "qrels.json", 'w', encoding='utf-8') as f:
        json.dump(qrels, f)

    print(f"Processed {len(queries)} queries from documents in {input_dir}")
    print(f"Results saved to {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process JSON documents for dataset creation")
    parser.add_argument(
        "--input_dir",
        default="copy/data/processed/pdf/arxiv/sections_concatenated",
        help="Directory containing input JSON documents")
    parser.add_argument("--output_dir",
                        default="copy/data/final/pdf/arxiv",
                        help="Directory to save processed outputs")

    args = parser.parse_args()
    convert_to_dataset(args.input_dir, args.output_dir)
