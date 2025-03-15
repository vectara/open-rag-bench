import os
import json
from tqdm import tqdm
from models.query_generator import OpenAIQueryGenerator
from models.mistral_ocr import MistralOCR

ocr = MistralOCR()
generator = OpenAIQueryGenerator()

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def generate_per_file(sections):
    title = sections['title']
    qa_pairs = [generator.generate(title, section) for section in tqdm(sections['sections'])]
    return qa_pairs

def generate_batch(input_dir, output_dir):
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith('.json'):
            markdown = read_json(os.path.join(input_dir, filename))
            sections = ocr.split_sections(markdown['text'])
            qa_pairs = generate_per_file(sections)
            write_json(qa_pairs, os.path.join(output_dir, filename))


if __name__ == "__main__":
    input_dir = "/home/renyi/projects/ragleaderboard/data/processed/pdf/arxiv"
    output_dir = "/home/renyi/projects/ragleaderboard/data/processed/pdf/arxiv/qa_pairs"
    generate_batch(input_dir, output_dir)