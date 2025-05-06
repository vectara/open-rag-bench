import os
import argparse
from joblib import Parallel, delayed, parallel_backend

from openragbench.utils import write_json
from openragbench.models.processors import MistralOCR

model = MistralOCR()


def process_and_save_pdf_md(pdf_path, output_dir):
    if os.path.exists(
            os.path.join(output_dir,
                         os.path.basename(pdf_path).replace(".pdf", ".json"))):
        print(f"File already exists: {pdf_path}")
        return
    markdown = model.convert_pdf_to_markdown(pdf_path)
    write_json(
        markdown,
        os.path.join(output_dir,
                     os.path.basename(pdf_path).replace(".pdf", ".json")))


def iterate_pdfs_parallel(input_directory, action, *args, **kwargs):
    """
    Iterates through all files in the given directory and its subdirectories,
    and calls the provided action function on each PDF file found.

    Parameters:
        input_directory (str): The path to the directory to search.
        action (callable): A function that processes a PDF file.
                           It must accept the PDF file path as its first argument.
        *args: Additional positional arguments to pass to the action function.
        **kwargs: Additional keyword arguments to pass to the action function.
    """
    for root, _, files in os.walk(input_directory):
        with parallel_backend('threading', n_jobs=10):
            Parallel(verbose=5)(
                delayed(action)(os.path.join(root, file), *args, **kwargs)
                for file in files
                if file.lower().endswith(".pdf"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",
                        type=str,
                        default="copy2/data/raw/pdf/arxiv")
    parser.add_argument("--output_dir",
                        type=str,
                        default="copy2/data/ocr/pdf/arxiv")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    iterate_pdfs_parallel(args.input_dir,
                          process_and_save_pdf_md,
                          output_dir=args.output_dir)
