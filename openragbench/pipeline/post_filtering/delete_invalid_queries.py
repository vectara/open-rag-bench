import os
import json
import argparse
from joblib import Parallel, delayed, parallel_backend

from openragbench.models.query_evaluator import StyleValidator

model = StyleValidator()


def delete_invalid_qa_queries(input_file_path: str,
                              output_file_path: str) -> tuple:
    filename = os.path.basename(input_file_path)

    try:
        # Read the input file
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract title and sections
        title = data.get('title', '')
        sections = data.get('sections', [])

        total_queries = 0
        valid_queries = 0

        # Process each section
        for section in sections:
            # Get the qa_pairs list
            qa_pairs = section.get('qa_pairs', [])
            total_queries += len(qa_pairs)

            # Filter out invalid queries
            valid_qa_pairs = []
            for qa_pair in qa_pairs:
                query = qa_pair.get('query', '')

                # Check if query is valid using the external evaluate function
                if model.evaluate(query):
                    valid_qa_pairs.append(qa_pair)
                    valid_queries += 1

            # Replace the original qa_pairs with the filtered list
            section['qa_pairs'] = valid_qa_pairs

        # Create processed data
        processed_data = {'title': title, 'sections': sections}

        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Write the processed data to the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)

        return filename, total_queries, valid_queries, None

    except FileNotFoundError:
        return filename, 0, 0, "File not found"
    except json.JSONDecodeError:
        return filename, 0, 0, "Invalid JSON format"
    except Exception as e:
        return filename, 0, 0, str(e)


def main(input_dir: str, output_dir: str, n_jobs: int = -1) -> None:
    """
    Process all JSON files in the input directory in parallel and save the results to the output directory.

    Args:
        input_dir: Directory containing input JSON files
        output_dir: Directory to save processed JSON files
        n_jobs: Number of jobs to run in parallel (-1 means using all processors)
    """
    # Check if input directory exists
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist.")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all JSON files in the input directory
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    if not json_files:
        print(f"Warning: No JSON files found in {input_dir}.")
        return

    print(f"Found {len(json_files)} JSON files to process.")

    # Create a list of input and output file paths
    input_files = [os.path.join(input_dir, f) for f in json_files]
    output_files = [os.path.join(output_dir, f) for f in json_files]

    # Process files in parallel using joblib
    print(f"Processing files using {n_jobs} parallel jobs...")
    with parallel_backend('threading', n_jobs=n_jobs):
        results = Parallel(verbose=10)(
            delayed(delete_invalid_qa_queries)(in_file, out_file)
            for in_file, out_file in zip(input_files, output_files))

    # Track total queries and valid queries
    total_all = 0
    valid_all = 0
    successful_files = 0
    failed_files = []

    # Process results
    print("\nResults:")
    for filename, total, valid, error in results:
        if error is None:
            total_all += total
            valid_all += valid
            successful_files += 1
            print(
                f"✓ {filename}: {total} queries, {valid} valid, {total-valid} discarded"
            )
        else:
            failed_files.append((filename, error))
            print(f"✗ {filename}: Failed - {error}")

    print(
        f"\nProcessing complete. {successful_files}/{len(json_files)} files processed successfully."
    )

    if failed_files:
        print("\nFailed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")

    print(f"\nProcessed files saved to {output_dir}.")
    print(
        f"Total: {total_all} queries found, {valid_all} valid ({total_all-valid_all} discarded)"
    )


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Filter out invalid queries from JSON files in parallel")
    parser.add_argument(
        "--input_dir",
        default=
        "copy/data/processed/pdf/arxiv/sections",
        help="Directory containing input JSON files")
    parser.add_argument(
        "--output_dir",
        default=
        "copy/data/processed/pdf/arxiv/sections_filtered",
        help="Directory to save processed JSON files")
    parser.add_argument(
        "--n_jobs",
        type=int,
        default=-1,
        help="Number of jobs to run in parallel (-1 means using all processors)"
    )

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.input_dir, args.output_dir, args.n_jobs)
