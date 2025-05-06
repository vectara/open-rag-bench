import os
from tqdm import tqdm

from openragbench.utils import read_json, write_json, read_config


def get_leaves(dictionary):
    """
    Collect all leaf values of a multi-level dictionary into a list.

    Args:
        dictionary (dict): A multi-level dictionary with equal-structured key-value pairs,
                          meaning at each level, the structure of the values is the same.

    Returns:
        list: A list containing all leaf values in the dictionary.
    """
    result = []

    def traverse(d):
        for key in sorted(d.keys()):  # Sort keys for consistent ordering
            value = d[key]
            if isinstance(value, dict):
                traverse(value)  # Recursively explore nested dictionaries
            else:
                result.append(value)  # Append leaf value to the result list

    traverse(dictionary)
    return [elem for l in result for elem in l]


def get_categories(config_path: str) -> list:
    """
    Get categories from the configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        list: List of categories.
    """
    config = read_config(config_path)
    return get_leaves(config['categories'])


def concat_sections_with_metadata(section_file: str, metadata_file: str,
                                  output_file: str) -> None:
    """
    Concatenate sections with metadata for each paper.

    Args:
        section_file (str): Path to the JSON file containing sections.
        metadata_file (str): Path to the JSON file containing metadata.
        output_file (str): Path to save the combined JSON file.
    """
    # Load the JSON files
    metadata = read_json(metadata_file)
    sections = read_json(section_file)

    sections.update(metadata)

    # Keep actual categories
    section_categories = [
        category for category in sections['categories']
        if category in categories
    ]
    sections['categories'] = section_categories

    # Save the combined data to a new JSON file
    write_json(sections, output_file)


if __name__ == "__main__":
    # Get categories from the configuration file
    config_path = 'configs/arxiv_configs.yaml'
    categories = get_categories(config_path)

    metadata_folder = 'copy/data/raw/pdf/arxiv/metadata'
    sections_folder = 'copy/data/processed/pdf/arxiv/sections'
    output_folder = 'copy/data/processed/pdf/arxiv/sections_concatenated'
    os.makedirs(output_folder, exist_ok=True)

    for filename in tqdm(os.listdir(sections_folder)):
        if filename.endswith('.json'):
            section_file = os.path.join(sections_folder, filename)
            metadata_file = os.path.join(metadata_folder, filename)
            output_file = os.path.join(output_folder, filename)
            concat_sections_with_metadata(section_file, metadata_file,
                                          output_file)
