import os
import json
import argparse
from tqdm import tqdm
from models.query_generator import OpenAIQueryGenerator
from models.mistral_ocr import MistralOCR

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def concat_section_with_qa_pairs(sections, qa_pairs):
    if len(sections["sections"]) != len(qa_pairs):
        raise ValueError("Mismatch between number of sections and QA pair lists")

    integrated_data = {
        "title": sections["title"],
        "sections": []
    }

    for i, section in enumerate(sections["sections"]):
        section_data = {
            "text": section,
            "qa_pairs": qa_pairs[i]
        }
        integrated_data["sections"].append(section_data)

    return integrated_data

def generate_per_file(sections):
    title = sections['title']
    qa_pairs = [generator.generate(title, section) for section in tqdm(sections['sections'])]
    return qa_pairs

def generate_batch(input_dir, output_dir, sections_dir):
    for filename in tqdm(os.listdir(input_dir)):
        if filename.endswith('.json'):
            markdown = read_json(os.path.join(input_dir, filename))
            sections = ocr.split_sections(markdown['text'])
            qa_pairs = generate_per_file(sections)
            write_json(qa_pairs, os.path.join(output_dir, filename))
            integrated_data = concat_section_with_qa_pairs(sections, qa_pairs)
            write_json(integrated_data, os.path.join(sections_dir, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default="/home/renyi/projects/ragleaderboard/data/processed/pdf/arxiv")
    parser.add_argument("--output_dir", type=str, default="/home/renyi/projects/ragleaderboard/data/processed/pdf/arxiv/qa_pairs")
    parser.add_argument("--sections_dir", type=str, default="/home/renyi/projects/ragleaderboard/data/processed/pdf/arxiv/sections")
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    sections_dir = args.sections_dir

    ocr = MistralOCR()
    generator = OpenAIQueryGenerator()

    generate_batch(input_dir, output_dir, sections_dir)