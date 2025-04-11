import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import argparse
from tqdm import tqdm
from utils import write_json
from models.processors import MistralOCR

model = MistralOCR()


def process_and_save_pdf_md(pdf_path, output_dir):
    markdown = model.convert_pdf_to_markdown(pdf_path)
    write_json(
        markdown,
        os.path.join(output_dir,
                     os.path.basename(pdf_path).replace(".pdf", ".json")))


def iterate_pdfs(input_directory, action, *args, **kwargs):
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
        for file in tqdm(files):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                action(pdf_path, *args, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="data/raw/pdf/arxiv")
    parser.add_argument("--output_dir", type=str, default="data/ocr/pdf/arxiv")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    iterate_pdfs(args.input_dir,
                 process_and_save_pdf_md,
                 output_dir=args.output_dir)
