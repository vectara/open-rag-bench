import os
from openragbench.models.query_evaluator import DocumentRelevanceFilter

if __name__ == "__main__":
    input_dir = "data/final/pdf/arxiv"
    output_dir = "data/final/pdf/arxiv/embeddings"
    corpus_path = os.path.join(input_dir, "corpus")
    queries_path = os.path.join(input_dir, "queries.json")
    os.makedirs(output_dir, exist_ok=True)

    model = DocumentRelevanceFilter()
    model.compute_query_embeddings(queries_path, output_dir)
    model.compute_section_embeddings(corpus_path, output_dir)