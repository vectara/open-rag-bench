import os
import numpy as np
import random
from collections import Counter, defaultdict
import logging

from openragbench.models.encoders import similarity_gpu as similarity
from openragbench.utils import read_json, write_json

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def filter_by_intersection(directory_path,
                           qrels_path,
                           output_path,
                           n_retrieval_results=50,
                           score_threshold=0.8):
    # Load the mappings
    query_id_to_index = read_json(
        os.path.join(directory_path, 'query_id_to_index.json'))
    section_id_to_index = read_json(
        os.path.join(directory_path, 'section_id_to_index.json'))
    qrels = read_json(qrels_path)

    # Get all model directories
    model_dirs = [
        d for d in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, d))
    ]

    # Store filtered query IDs for each model
    model_filtered_queries = {}

    # Process each model
    for model_name in model_dirs:
        logger.info(f"Processing model: {model_name}")

        model_path = os.path.join(directory_path, model_name)
        query_emb_path = os.path.join(model_path, 'query_embeddings.npy')
        section_emb_path = os.path.join(model_path, 'section_embeddings.npy')
        similarity_scores_path = os.path.join(model_path,
                                              'similarity_scores.npy')

        # Skip if embedding files don't exist
        if not (os.path.exists(query_emb_path) and
                os.path.exists(section_emb_path)):
            logger.warning(
                f"Embedding files not found for {model_name}, skipping...")
            continue

        # Check if similarity scores already exist
        if os.path.exists(similarity_scores_path):
            logger.info(
                f"Loading precomputed similarity scores for {model_name}...")
            similarity_scores = np.load(similarity_scores_path)
        else:
            # Load embeddings
            query_embeddings = np.load(query_emb_path)
            section_embeddings = np.load(section_emb_path)

            logger.info(f"Computing similarity scores for {model_name}...")
            # Compute similarity scores (cosine similarity)
            similarity_scores = similarity(query_embeddings, section_embeddings)

            # Save similarity scores
            logger.info(f"Saving similarity scores for {model_name}...")
            np.save(similarity_scores_path, similarity_scores)

        # Initialize set of all query IDs
        filtered_query_ids = set(query_id_to_index.keys())
        initial_count = len(filtered_query_ids)

        # Stage 1: Check if relevant section is in top N results
        logger.info(
            f"Starting Stage 1 filtering for {model_name} (top {n_retrieval_results})..."
        )
        for query_id in list(filtered_query_ids):
            # Skip if query not in qrels
            if query_id not in qrels:
                filtered_query_ids.remove(query_id)
                continue

            query_idx = query_id_to_index[query_id]
            doc_id = qrels[query_id]['doc_id']
            section_id = str(qrels[query_id]['section_id'])

            # Skip if document or section not in mappings
            if doc_id not in section_id_to_index or section_id not in section_id_to_index[
                    doc_id]:
                filtered_query_ids.remove(query_id)
                continue

            # Get index of relevant section
            relevant_section_idx = section_id_to_index[doc_id][section_id]

            # Get top N sections for this query
            query_sim_scores = similarity_scores[query_idx]
            top_n_indices = np.argsort(
                query_sim_scores)[::-1][:
                                        n_retrieval_results]  # Descending order

            # Remove query if relevant section not in top N
            if relevant_section_idx not in top_n_indices:
                filtered_query_ids.remove(query_id)

        stage1_count = len(filtered_query_ids)
        logger.info(
            f"Stage 1 complete. Remaining queries: {stage1_count}/{initial_count}"
        )

        # Stage 2: Check if similarity with relevant section > threshold
        logger.info(
            f"Starting Stage 2 filtering for {model_name} (threshold {score_threshold})..."
        )
        for query_id in list(filtered_query_ids):
            query_idx = query_id_to_index[query_id]
            doc_id = qrels[query_id]['doc_id']
            section_id = str(qrels[query_id]['section_id'])
            relevant_section_idx = section_id_to_index[doc_id][section_id]

            # Get similarity score with relevant section
            sim_score = similarity_scores[query_idx][relevant_section_idx]

            # Remove query if similarity < threshold
            if sim_score < score_threshold:
                filtered_query_ids.remove(query_id)

        stage2_count = len(filtered_query_ids)
        logger.info(
            f"Stage 2 complete. Remaining queries: {stage2_count}/{stage1_count}"
        )

        # Store filtered queries for this model
        model_filtered_queries[model_name] = list(filtered_query_ids)

    # Find intersection of filtered query IDs across all models
    if not model_filtered_queries:
        logger.warning("No valid models found.")
        intersection = set()
    else:
        filtered_sets = [set(ids) for ids in model_filtered_queries.values()]
        intersection = filtered_sets[0]
        for s in filtered_sets[1:]:
            intersection = intersection.intersection(s)

    # Convert to list for JSON serialization
    intersection_list = list(intersection)

    # Save results
    output_file = os.path.join(output_path,
                               'filtered_queries_intersection.json')
    write_json(intersection_list, output_file)

    # Also save individual model results
    model_output_file = os.path.join(output_path, 'model_filtered_queries.json')
    write_json(model_filtered_queries, model_output_file)

    logger.info(f"Final intersection contains {len(intersection_list)} queries")
    logger.info(f"Results saved to {output_file}")

    return intersection_list


def filter_by_average(directory_path,
                      qrels_path,
                      output_path,
                      n_retrieval_results=50,
                      score_threshold=0.8):
    # Load the mappings
    query_id_to_index = read_json(
        os.path.join(directory_path, 'query_id_to_index.json'))
    section_id_to_index = read_json(
        os.path.join(directory_path, 'section_id_to_index.json'))
    qrels = read_json(qrels_path)

    # Get all model directories
    model_dirs = [
        d for d in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, d))
    ]

    # Store similarity scores for each model
    all_model_similarity_scores = []
    valid_models = []

    # Process each model to get similarity scores
    for model_name in model_dirs:
        logger.info(f"Processing model: {model_name}")

        model_path = os.path.join(directory_path, model_name)
        query_emb_path = os.path.join(model_path, 'query_embeddings.npy')
        section_emb_path = os.path.join(model_path, 'section_embeddings.npy')
        similarity_scores_path = os.path.join(model_path,
                                              'similarity_scores.npy')

        # Skip if embedding files don't exist
        if not (os.path.exists(query_emb_path) and
                os.path.exists(section_emb_path)):
            logger.warning(
                f"Embedding files not found for {model_name}, skipping...")
            continue

        # Check if similarity scores already exist
        if os.path.exists(similarity_scores_path):
            logger.info(
                f"Loading precomputed similarity scores for {model_name}...")
            similarity_scores = np.load(similarity_scores_path)
        else:
            # Load embeddings
            query_embeddings = np.load(query_emb_path)
            section_embeddings = np.load(section_emb_path)

            logger.info(f"Computing similarity scores for {model_name}...")
            # Compute similarity scores (cosine similarity)
            similarity_scores = similarity(query_embeddings, section_embeddings)

            # Save similarity scores
            logger.info(f"Saving similarity scores for {model_name}...")
            np.save(similarity_scores_path, similarity_scores)

        # Add to our collection
        all_model_similarity_scores.append(similarity_scores)
        valid_models.append(model_name)

    if not all_model_similarity_scores:
        logger.error("No valid models found with similarity scores. Exiting.")
        return []

    # Compute average similarity scores across all models
    logger.info(
        f"Computing average similarity scores across {len(valid_models)} models..."
    )
    avg_similarity_scores = np.mean(all_model_similarity_scores, axis=0)

    # Now apply two-stage filtering on the averaged similarity scores

    # Initialize set of all query IDs
    filtered_query_ids = set(query_id_to_index.keys())
    initial_count = len(filtered_query_ids)

    # Stage 1: Check if relevant section is in top N results
    logger.info(
        f"Starting Stage 1 filtering on averaged scores (top {n_retrieval_results})..."
    )
    for query_id in list(filtered_query_ids):
        # Skip if query not in qrels
        if query_id not in qrels:
            filtered_query_ids.remove(query_id)
            continue

        query_idx = query_id_to_index[query_id]
        doc_id = qrels[query_id]['doc_id']
        section_id = str(qrels[query_id]['section_id'])

        # Skip if document or section not in mappings
        if doc_id not in section_id_to_index or section_id not in section_id_to_index[
                doc_id]:
            filtered_query_ids.remove(query_id)
            continue

        # Get index of relevant section
        relevant_section_idx = section_id_to_index[doc_id][section_id]

        # Get top N sections for this query
        query_sim_scores = avg_similarity_scores[query_idx]
        top_n_indices = np.argsort(
            query_sim_scores)[::-1][:n_retrieval_results]  # Descending order

        # Remove query if relevant section not in top N
        if relevant_section_idx not in top_n_indices:
            filtered_query_ids.remove(query_id)

    stage1_count = len(filtered_query_ids)
    logger.info(
        f"Stage 1 complete. Remaining queries: {stage1_count}/{initial_count}")

    # Stage 2: Check if similarity with relevant section > threshold
    logger.info(
        f"Starting Stage 2 filtering on averaged scores (threshold {score_threshold})..."
    )
    for query_id in list(filtered_query_ids):
        query_idx = query_id_to_index[query_id]
        doc_id = qrels[query_id]['doc_id']
        section_id = str(qrels[query_id]['section_id'])
        relevant_section_idx = section_id_to_index[doc_id][section_id]

        # Get similarity score with relevant section
        sim_score = avg_similarity_scores[query_idx][relevant_section_idx]

        # Remove query if similarity < threshold
        if sim_score < score_threshold:
            filtered_query_ids.remove(query_id)

    stage2_count = len(filtered_query_ids)
    logger.info(
        f"Stage 2 complete. Remaining queries: {stage2_count}/{stage1_count}")

    # Convert to list for JSON serialization
    filtered_query_list = list(filtered_query_ids)

    # Save results
    output_file = os.path.join(output_path, 'filtered_queries_averaged.json')
    write_json(filtered_query_list, output_file)

    logger.info(
        f"Final filtered set contains {len(filtered_query_list)} queries")
    logger.info(f"Results saved to {output_file}")

    return filtered_query_list


def deduplicate_queries(directory_path,
                        filtered_queries_path,
                        output_path,
                        similarity_threshold=0.95):
    """
    Deduplicate queries based on average similarity across models.

    Args:
        directory_path: Path to the main directory containing model subfolders
        filtered_queries_path: Path to the JSON file containing filtered query IDs
        similarity_threshold: Threshold for considering queries as similar (default: 0.95)
        output_file: Path to save the deduplicated query list

    Returns:
        List of deduplicated query IDs
    """
    # Load filtered queries
    filtered_queries = read_json(filtered_queries_path)

    logger.info(f"Loaded {len(filtered_queries)} filtered queries")

    # Load query ID to index mapping
    query_id_to_index_path = os.path.join(directory_path,
                                          'query_id_to_index.json')
    query_id_to_index = read_json(query_id_to_index_path)

    # Get indices of filtered queries
    filtered_query_indices = [
        query_id_to_index[qid]
        for qid in filtered_queries
        if qid in query_id_to_index
    ]

    if not filtered_query_indices:
        logger.error(
            "None of the filtered queries were found in query_id_to_index mapping"
        )
        return []

    # Get all model directories
    model_dirs = [
        d for d in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, d))
    ]

    # Store query-query similarity matrices for each model
    all_query_similarities = []
    valid_models = []

    # Process each model
    for model_name in model_dirs:
        logger.info(f"Processing model: {model_name}")

        query_emb_path = os.path.join(directory_path, model_name,
                                      'query_embeddings.npy')

        # Skip if query embeddings don't exist
        if not os.path.exists(query_emb_path):
            logger.warning(
                f"Query embeddings not found for {model_name}, skipping...")
            continue

        # Load query embeddings
        query_embeddings = np.load(query_emb_path)

        # Filter to only include embeddings for the filtered queries
        filtered_embeddings = query_embeddings[filtered_query_indices]

        # Compute query-query similarity
        logger.info(f"Computing query-query similarity for {model_name}...")
        query_query_similarity = similarity(filtered_embeddings,
                                            filtered_embeddings)

        all_query_similarities.append(query_query_similarity)
        valid_models.append(model_name)

    if not all_query_similarities:
        logger.error("No valid models found. Exiting.")
        return []

    # Compute average query-query similarity across all models
    logger.info(
        f"Computing average query-query similarity across {len(valid_models)} models..."
    )
    avg_query_similarity = np.mean(all_query_similarities, axis=0)

    # Set diagonal to 0 to avoid self-similarity
    np.fill_diagonal(avg_query_similarity, 0)

    # Cluster queries based on similarity threshold
    logger.info(
        f"Clustering queries with similarity threshold {similarity_threshold}..."
    )

    # Initialize clusters
    clusters = []
    assigned_indices = set()

    # Iterate through all filtered query indices
    for i in range(len(filtered_query_indices)):
        if i in assigned_indices:
            continue  # Skip if already assigned to a cluster

        # Find all queries similar to this one
        similar_indices = np.where(
            avg_query_similarity[i] >= similarity_threshold)[0]

        if len(similar_indices) == 0:
            # No similar queries, add as singleton cluster
            clusters.append([i])
            assigned_indices.add(i)
        else:
            # Create a new cluster with all similar queries
            new_cluster = [i] + [idx for idx in similar_indices if idx != i]
            clusters.append(new_cluster)
            assigned_indices.update(new_cluster)

    # For each cluster, find the query with highest average similarity to other queries in the cluster
    logger.info("Selecting representative queries from each cluster...")
    representative_indices = []

    for cluster in clusters:
        if len(cluster) == 1:
            # Singleton cluster, keep the only query
            representative_indices.append(cluster[0])
        else:
            # For larger clusters, find the query with highest average similarity to others
            cluster_similarity = avg_query_similarity[cluster, :][:, cluster]
            avg_similarities = np.sum(cluster_similarity, axis=1) / (
                len(cluster) - 1)  # Exclude self
            best_query_idx = cluster[np.argmax(avg_similarities)]
            representative_indices.append(best_query_idx)

    # Map representative indices back to query IDs
    deduplicated_queries = [
        filtered_queries[idx] for idx in representative_indices
    ]

    # Log clustering stats
    logger.info(f"Original query count: {len(filtered_queries)}")
    logger.info(f"Clusters found: {len(clusters)}")
    logger.info(f"Deduplicated query count: {len(deduplicated_queries)}")
    logger.info(
        f"Removed {len(filtered_queries) - len(deduplicated_queries)} duplicate queries"
    )

    # Save results
    output_file = os.path.join(output_path, "deduplicated_queries.json")
    write_json(deduplicated_queries, output_file)

    logger.info(f"Deduplicated queries saved to {output_file}")

    return deduplicated_queries


def balance_queries_by_document(directory_path,
                                queries_per_doc_threshold=10,
                                random_seed=2):
    """
    Balance the number of queries per document by applying a threshold.

    Args:
        directory_path: Path to the directory containing the JSON files
        queries_per_doc_threshold: Maximum number of queries to keep per document
        random_seed: Seed for random sampling to ensure reproducibility

    Returns:
        List of balanced query IDs
    """
    # Set random seed for reproducibility
    random.seed(random_seed)

    # Load deduplicated queries
    deduplicated_queries_path = os.path.join(directory_path,
                                             'deduplicated_queries.json')
    deduplicated_queries = read_json(deduplicated_queries_path)

    if not deduplicated_queries:
        logger.error("No deduplicated queries found.")
        return []

    logger.info(f"Loaded {len(deduplicated_queries)} deduplicated queries")

    # Load qrels to get document-query mappings
    qrels_path = os.path.join(directory_path, 'qrels.json')
    qrels = read_json(qrels_path)

    if not qrels:
        logger.error("Failed to load qrels.json")
        return deduplicated_queries  # Return original list if qrels can't be loaded

    # Create a mapping from document IDs to their associated queries
    doc_to_queries = defaultdict(list)

    # Only consider queries that are in the deduplicated list
    for query_id in deduplicated_queries:
        if query_id in qrels:
            doc_id = qrels[query_id].get('doc_id')
            if doc_id:
                doc_to_queries[doc_id].append(query_id)

    logger.info(
        f"Found {len(doc_to_queries)} documents with associated queries")

    # Apply balancing
    balanced_queries = []

    for doc_id, queries in doc_to_queries.items():
        if len(queries) > queries_per_doc_threshold:
            # Too many queries for this document, randomly sample
            logger.info(
                f"Document {doc_id} has {len(queries)} queries, sampling down to {queries_per_doc_threshold}"
            )
            selected_queries = random.sample(queries, queries_per_doc_threshold)
            balanced_queries.extend(selected_queries)
        else:
            # Number of queries is within threshold, keep all
            logger.info(
                f"Document {doc_id} has {len(queries)} queries, keeping all")
            balanced_queries.extend(queries)

    # Check for any queries that were in the deduplicated list but not in qrels
    missing_in_qrels = [qid for qid in deduplicated_queries if qid not in qrels]
    if missing_in_qrels:
        logger.warning(
            f"Found {len(missing_in_qrels)} queries that were in deduplicated list but not in qrels"
        )
        # Add these to the balanced list since we can't filter them by document
        balanced_queries.extend(missing_in_qrels)
        logger.info(
            f"Added {len(missing_in_qrels)} queries that were missing in qrels to the balanced list"
        )

    # Remove any duplicates that might have been introduced
    balanced_queries = list(set(balanced_queries))

    logger.info(f"Final balanced query count: {len(balanced_queries)}")

    # Save the balanced queries
    output_path = os.path.join(directory_path, 'queries_subset.json')
    write_json(balanced_queries, output_path)

    return balanced_queries


def print_filtered_query_stats(directory_path,
                               query_file='balanced_queries.json'):
    """Print statistics about filtered queries"""
    # Load filtered queries
    filtered_queries_path = os.path.join(directory_path, query_file)
    filtered_queries = read_json(filtered_queries_path)

    if not filtered_queries:
        logger.error(
            "No filtered queries found. Make sure the first script was run successfully."
        )
        return

    # Load query information
    queries_info = read_json(os.path.join(directory_path, 'queries.json'))

    # Load document mapping
    qrels = read_json(os.path.join(directory_path, 'qrels.json'))

    # Initialize counters
    type_counter = Counter()
    source_counter = Counter()
    doc_id_counter = Counter()

    # Count for each filtered query
    for query_id in filtered_queries:
        # Skip if query not in query info
        if query_id not in queries_info:
            logger.warning(f"Query ID {query_id} not found in queries.json")
            continue

        query_type = queries_info[query_id].get('type', 'unknown')
        query_source = queries_info[query_id].get('source', 'unknown')

        type_counter[query_type] += 1
        source_counter[query_source] += 1

        # Get doc_id if available
        if query_id in qrels:
            doc_id = qrels[query_id].get('doc_id', 'unknown')
            doc_id_counter[doc_id] += 1
        else:
            logger.warning(f"Query ID {query_id} not found in qrels.json")

    # Print results
    logger.info(f"Total filtered queries: {len(filtered_queries)}")

    print("\n=== QUERY TYPE STATISTICS ===")
    print(f"Total types: {len(type_counter)}")
    for query_type, count in sorted(type_counter.items()):
        percentage = (count / len(filtered_queries)) * 100
        print(f"  {query_type}: {count} ({percentage:.1f}%)")

    print("\n=== QUERY SOURCE STATISTICS ===")
    print(f"Total sources: {len(source_counter)}")
    for source, count in sorted(source_counter.items()):
        percentage = (count / len(filtered_queries)) * 100
        print(f"  {source}: {count} ({percentage:.1f}%)")

    print("\n=== DOCUMENT ID STATISTICS ===")
    print(f"Total unique documents: {len(doc_id_counter)}")
    for doc_id, count in sorted(doc_id_counter.items(),
                                key=lambda x: x[1],
                                reverse=True):
        percentage = (count / len(filtered_queries)) * 100
        print(f"  {doc_id}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    filter_by_intersection("data/final/pdf/arxiv/embeddings",
                           "data/final/pdf/arxiv/qrels.json",
                           "data/final/pdf/arxiv",
                           n_retrieval_results=25,
                           score_threshold=0.8)

    filter_by_average("data/final/pdf/arxiv/embeddings",
                      "data/final/pdf/arxiv/qrels.json",
                      "data/final/pdf/arxiv",
                      n_retrieval_results=25,
                      score_threshold=0.9)

    deduplicate_queries(
        "data/final/pdf/arxiv/embeddings",
        "data/final/pdf/arxiv/filtered_queries_intersection.json",
        "data/final/pdf/arxiv",
        similarity_threshold=0.6)

    balance_queries_by_document("data/final/pdf/arxiv",
                                queries_per_doc_threshold=10,
                                random_seed=2)

    # print_filtered_query_stats("data/final/pdf/arxiv")
    print_filtered_query_stats("data/final/pdf/arxiv", "queries_subset.json")
