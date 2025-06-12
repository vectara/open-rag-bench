import os
import json
import argparse
import random
import numpy as np

from openragbench.utils import read_json, write_json
from openragbench.models.encoders import similarity_gpu


def find_hard_negatives(input_dir, k):
    # Load the data
    query_embeddings = np.load(
        os.path.join(input_dir, 'StellaEncoder/query_embeddings.npy'))
    section_embeddings = np.load(
        os.path.join(input_dir, 'StellaEncoder/section_embeddings.npy'))

    with open(os.path.join(input_dir, 'query_id_to_index.json'), 'r') as f:
        query_id_to_index = json.load(f)

    with open(os.path.join(input_dir, 'section_id_to_index.json'), 'r') as f:
        section_id_to_index = json.load(f)

    # Load the subset of query IDs
    queries_subset_path = os.path.join(input_dir, 'queries_subset.json')
    with open(queries_subset_path, 'r') as f:
        query_ids_subset = set(json.load(f))

    print(f"Loaded subset of {len(query_ids_subset)} query IDs to process")

    # Get the indices for the subset of queries
    query_indices_to_process = []
    for query_id, query_idx in query_id_to_index.items():
        if query_id in query_ids_subset:
            query_indices_to_process.append(query_idx)

    print(
        f"Found {len(query_indices_to_process)} corresponding query indices to process"
    )

    # Check if similarity matrix is already computed and saved
    similarity_matrix_path = os.path.join(input_dir, 'similarity_matrix.npy')
    similarity_matrix_2_path = os.path.join(input_dir,
                                            'similarity_matrix_2.npy')

    # Process each query row-by-row instead of loading entire matrices
    if not os.path.exists(similarity_matrix_path):
        print("Computing similarity matrix...")
        similarity_matrix = similarity_gpu(query_embeddings, section_embeddings)
        np.save(similarity_matrix_path, similarity_matrix)
        print("Similarity matrix saved for future use.")

    # Check if second similarity matrix exists
    has_matrix_2 = os.path.exists(similarity_matrix_2_path)
    if has_matrix_2:
        print(
            "Second similarity matrix found. Will process with both matrices.")
    else:
        print("No second similarity matrix found. Using only the first matrix.")

    # Initialize memory-mapped arrays for reading
    sim_matrix_1 = np.load(similarity_matrix_path, mmap_mode='r')
    sim_matrix_2 = np.load(similarity_matrix_2_path,
                           mmap_mode='r') if has_matrix_2 else None

    # Process only the subset of queries to find relevant section indices
    relevant_section_indices = set()

    print(
        f"Processing {len(query_indices_to_process)} queries from the subset to find top-{k} sections..."
    )
    for i, query_idx in enumerate(query_indices_to_process):
        if i % 100 == 0:
            print(f"Processing query {i}/{len(query_indices_to_process)}...")

        # Get current query's similarity scores from first matrix
        scores = sim_matrix_1[query_idx].copy(
        )  # Copy to avoid issues with mmap

        if has_matrix_2:
            # Get scores from second matrix and combine
            scores_2 = sim_matrix_2[query_idx].copy()

            # Find top-k across both matrices
            # We'll use argpartition which is faster than argsort for just finding top k
            if len(scores) + len(scores_2) <= k:
                # If we have fewer sections than k, just take all indices
                top_indices = list(range(len(scores)))
            else:
                # Create virtual combined array for ranking
                combined_scores = np.concatenate([scores, scores_2])
                top_k_partition = np.argpartition(combined_scores, -k)[-k:]
                # Get original indices that are in top-k and part of first matrix
                top_indices = [
                    idx for idx in top_k_partition if idx < len(scores)
                ]
        else:
            # Using just the first matrix
            if len(scores) <= k:
                top_indices = list(range(len(scores)))
            else:
                top_k_partition = np.argpartition(scores, -k)[-k:]
                top_indices = list(top_k_partition)

        # Update the set of relevant section indices
        relevant_section_indices.update(top_indices)

    print(
        f"Found {len(relevant_section_indices)} relevant section indices across the subset of queries."
    )

    # Find hard negative documents
    hard_negative_docs = []

    # Iterate through documents
    doc_count = len(section_id_to_index)
    print(f"Checking {doc_count} documents for hard negatives...")

    for doc_id, sections_dict in section_id_to_index.items():
        # Check if all sections of this document are irrelevant
        is_hard_negative = True
        for section_id, section_idx in sections_dict.items():
            if section_idx in relevant_section_indices:
                # This section is relevant to at least one query
                is_hard_negative = False
                break

        if is_hard_negative:
            hard_negative_docs.append(doc_id)

    # Save the hard negative documents to a JSON file
    output_file = os.path.join(input_dir, 'hard_negative_docs.json')
    with open(output_file, 'w') as f:
        json.dump(hard_negative_docs, f, indent=4)

    # Log the number of hard negative documents
    print(f"Found {len(hard_negative_docs)} hard negative documents.")

    return hard_negative_docs


def sample_hard_negatives(categories_dir, hard_negative_documents, n=600):
    """
    Sample n document IDs from hard_negative_documents, with an equal number from each category.

    Args:
        categories_dir (str): Path to the directory containing category subfolders.
        hard_negative_documents (list): List of candidate document IDs.
        n (int): Total number of document IDs to sample.

    Returns:
        list: Sampled document IDs with equal distribution across categories.
    """
    # Ensure n is divisible by 8
    if n % 8 != 0:
        raise ValueError("n must be divisible by 8 for equal distribution")

    n_per_category = n // 8

    # Get all category folders
    category_folders = [
        folder for folder in os.listdir(categories_dir)
        if os.path.isdir(os.path.join(categories_dir, folder))
    ]

    # Ensure we have exactly 8 categories
    if len(category_folders) != 8:
        raise ValueError(
            f"Expected 8 categories, found {len(category_folders)}")

    # Create a dictionary mapping document IDs to their categories
    doc_to_category = {}
    for category in category_folders:
        category_path = os.path.join(categories_dir, category)
        for filename in os.listdir(category_path):
            if filename.endswith('.pdf'):
                doc_id = os.path.splitext(filename)[0]  # Remove .pdf extension
                doc_to_category[doc_id] = category

    # Group hard negative candidates by category
    candidates_by_category = {category: [] for category in category_folders}

    for doc_id in hard_negative_documents:
        if doc_id in doc_to_category:
            category = doc_to_category[doc_id]
            candidates_by_category[category].append(doc_id)

    # Sample equal number of documents from each category
    sampled_docs = []

    for category, candidates in candidates_by_category.items():
        if len(candidates) < n_per_category:
            raise ValueError(
                f"Not enough hard negative candidates in category '{category}'. "
                f"Needed {n_per_category}, but only found {len(candidates)}")

        sampled_docs.extend(random.sample(candidates, n_per_category))

    print(
        f"Sampled {len(sampled_docs)} documents with equal distribution across categories"
    )

    return sampled_docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Find hard negative documents.')
    parser.add_argument(
        '--input_dir',
        type=str,
        default=
        "copy/data/final/pdf/arxiv/embeddings",
        help='Directory containing the data files')
    parser.add_argument('--k',
                        type=int,
                        default=50,
                        help='Number of top-k retrieval results to consider')

    args = parser.parse_args()

    hard_negatives = find_hard_negatives(args.input_dir, args.k)

    categories_dir = "copy/data/raw/pdf/arxiv/pdf"
    hard_negative_documents = read_json(
        "copy/data/final/pdf/arxiv/embeddings/hard_negative_docs.json"
    )
    sampled_docs = sample_hard_negatives(categories_dir,
                                         hard_negative_documents)
    write_json(
        sampled_docs,
        "copy/data/final/pdf/arxiv/embeddings/hard_negative_docs_sampled.json"
    )
