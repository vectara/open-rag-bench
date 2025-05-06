import json
import os
from joblib import Parallel, delayed, Memory, parallel_backend

from openragbench.models.query_evaluator import TypeValidator

# Set up caching for the validator results
cache_dir = '.joblib_cache'
memory = Memory(cache_dir, verbose=0)


# Cache the validator evaluation to avoid repeated computation for the same queries
@memory.cache
def cached_evaluate(query):
    validator = TypeValidator()
    return validator.evaluate(query)


def process_single_query(query_id, query_data):
    """Process a single query and return the updated query data"""
    query_text = query_data.get('query', '')
    current_type = query_data.get('type', '')

    # Evaluate the query type
    is_abstractive = cached_evaluate(query_text)
    correct_type = "abstractive" if is_abstractive else "extractive"

    # Check if there's a mismatch and update
    if current_type != correct_type:
        # Create a new dictionary to avoid modifying the original
        updated_data = query_data.copy()
        updated_data['type'] = correct_type
        return query_id, updated_data, True  # True indicates a change was made

    return query_id, query_data, False  # False indicates no change


def validate_query_types_parallel(input_dir, n_jobs=-1):
    """Validate query types in parallel"""
    # Input and output file paths
    input_path = os.path.join(input_dir, 'queries.json')
    output_path = os.path.join(input_dir, 'queries_checked.json')

    # Load the queries dictionary from JSON file
    try:
        with open(input_path, 'r') as file:
            queries_dict = json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {input_path}")
        return

    print(f"Processing {len(queries_dict)} queries in parallel...")

    # Process all queries in parallel
    with parallel_backend('threading', n_jobs=n_jobs):
        results = Parallel(verbose=10)(
            delayed(process_single_query)(query_id, query_data)
            for query_id, query_data in queries_dict.items())

    # Count of changes made
    changes_count = 0

    # Update the dictionary with the results
    for query_id, updated_data, changed in results:
        if changed:
            queries_dict[query_id] = updated_data
            changes_count += 1

    # Save the updated dictionary to the output file
    try:
        with open(output_path, 'w') as file:
            json.dump(queries_dict, file, indent=2)
        print(f"Successfully saved updated queries to {output_path}")
        print(f"Total changes made: {changes_count}")

        # Count and print the number of abstractive and extractive queries
        abstractive_count = sum(1 for data in queries_dict.values()
                                if data.get('type') == 'abstractive')
        extractive_count = sum(1 for data in queries_dict.values()
                               if data.get('type') == 'extractive')

        print(f"\nFinal Query Type Counts:")
        print(f"- Abstractive queries: {abstractive_count}")
        print(f"- Extractive queries: {extractive_count}")
        print(f"- Total queries: {len(queries_dict)}")

        # Verify count
        if abstractive_count + extractive_count != len(queries_dict):
            print(
                f"Warning: Some queries may have missing or invalid type values."
            )

    except Exception as e:
        print(f"Error saving output file: {e}")

    # Clean up cache if needed (uncomment to clear cache after running)
    memory.clear()


if __name__ == "__main__":
    validate_query_types_parallel(
        "official/pdf/arxiv")
