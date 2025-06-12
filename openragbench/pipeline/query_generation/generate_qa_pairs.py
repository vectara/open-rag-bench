import os
import argparse
from tqdm import tqdm
from joblib import Parallel, delayed, Memory, parallel_backend

from openragbench.models.query_generator import QueryGenerator
from openragbench.models.processors import MarkdownProcessor
from openragbench.utils import read_json, write_json

CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)
MEMORY = Memory(CACHE_DIR, verbose=0)
PROCESSOR = MarkdownProcessor()


@MEMORY.cache
def generate_per_file(sections):
    title = sections['title']
    with parallel_backend('threading', n_jobs=30):
        qa_pairs = Parallel(verbose=5)(
            delayed(generator.generate)(title,
                                        text=section['text'],
                                        table_data=section['tables'],
                                        image_data=section['images'])
            for section in sections['sections'])
    return qa_pairs


def generate_batch(input_dir, cache_dir, output_dir):
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith('.json'):
            print(f"Processing {filename}...")
            markdown = read_json(os.path.join(input_dir, filename))
            sections = PROCESSOR.split_sections(markdown)
            # qa_pairs = generate_per_file(sections)
            qa_pairs = [[] for _ in range(len(sections['sections']))]
            # write_json(qa_pairs, os.path.join(cache_dir, filename))
            integrated_data = PROCESSOR.concat_section_with_qa_pairs(
                sections, qa_pairs)
            write_json(integrated_data, os.path.join(output_dir, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_dir",
        type=str,
        default="copy/data/ocr/pdf/arxiv")
    # default="nano_experiment/data/raw")
    parser.add_argument(
        "--cache_dir",
        type=str,
        default=
        "copy/data/processed/pdf/arxiv/qa_pairs"
    )
    # default="nano_experiment/data/qa_pairs")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=
        "copy/data/processed/pdf/arxiv/sections"
    )
    # default="nano_experiment/data/sections")
    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    args = parser.parse_args()
    input_dir = args.input_dir
    cache_dir = args.cache_dir
    output_dir = args.output_dir
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    model = args.model

    generator = QueryGenerator(model=model)

    generate_batch(input_dir, cache_dir, output_dir)
