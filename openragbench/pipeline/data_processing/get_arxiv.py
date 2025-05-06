import os
import time
import random
import json
import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, List, Set
from tqdm import tqdm

from openragbench.utils import read_yaml


def get_response(query: str | None = None,
                 metadata: Dict[str, str] = {},
                 max_results: int = 100,
                 start: int = 0) -> str:
    """
    Retrieve an API response from arxiv based on a search query and metadata.

    Args:
        query (Optional[str]): The search query. If provided, it will be URL-encoded
                               and added to the metadata.
        metadata (Dict[str, str]): A dictionary of metadata parameters for the query.
        max_results (int): The maximum number of results to fetch.
        start (int): Starting index for results.

    Returns:
        str: The response data decoded as a UTF-8 string.
    """
    if query is not None:
        metadata['all'] = urllib.parse.quote(query)
    combined_query = '+AND+'.join([f'{k}:{v}' for k, v in metadata.items()])
    url = (
        f'http://export.arxiv.org/api/query?search_query={combined_query}'
        f'&start={start}&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending'
    )

    # Add retry mechanism with backoff
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            if attempt < max_retries - 1:
                # Wait with exponential backoff before retrying
                wait_time = (2**attempt) + random.uniform(0, 1)
                print(
                    f"API request failed. Retrying in {wait_time:.2f} seconds..."
                )
                time.sleep(wait_time)
            else:
                print(
                    f"Failed to get response after {max_retries} attempts: {e}")
                raise


def download_pdfs(response: str, download_dir: str, existing_ids: Set[str],
                  target_count: int, current_count: int) -> List[str]:
    """
    Parse an arxiv API response and download the corresponding PDFs.

    Args:
        response (str): The XML response from the arxiv API.
        download_dir (str): The directory where downloaded PDFs will be saved.
        existing_ids (Set[str]): Set of paper IDs to avoid downloading.
        target_count (int): The target number of PDFs to download for this category.
        current_count (int): The current number of PDFs already downloaded for this category.

    Returns:
        List[str]: List of successfully downloaded paper IDs.
    """
    os.makedirs(download_dir, exist_ok=True)
    downloaded_ids = []

    try:
        root = ET.fromstring(response)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', ns):
            # Skip if we've reached our target
            if current_count + len(downloaded_ids) >= target_count:
                break

            try:
                # Extract paper ID from the entry
                id_elem = entry.find('atom:id', ns)
                if id_elem is not None and id_elem.text:
                    full_id = id_elem.text
                    paper_id = full_id.split('/abs/')[-1]
                else:
                    print("Skipping entry with no ID")
                    continue

                # Skip if it's in the existing IDs
                if paper_id in existing_ids or paper_id in downloaded_ids:
                    print(f"Skipping existing paper: {paper_id}")
                    continue

                title = entry.find('atom:title', ns).text.strip().replace(
                    '\n', ' ').replace(' ', '_')
                pdf_url = None

                for link in entry.findall('atom:link', ns):
                    if link.attrib.get('title') == 'pdf':
                        pdf_url = link.attrib['href']
                        break

                if pdf_url:
                    file_name = paper_id + '.pdf'
                    file_path = os.path.join(download_dir, file_name)

                    if os.path.exists(file_path):
                        print(f"PDF already exists for entry: {title}")
                        continue

                    print(f"Downloading {pdf_url} to {file_path}")
                    try:
                        # Add retry mechanism for downloads
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                urllib.request.urlretrieve(pdf_url, file_path)
                                # Successfully downloaded
                                downloaded_ids.append(paper_id)
                                print(
                                    f"Successfully downloaded {paper_id} ({len(downloaded_ids) + current_count}/{target_count})"
                                )
                                break
                            except Exception as e:
                                if attempt < max_retries - 1:
                                    wait_time = (2**attempt) + random.uniform(
                                        0, 1)
                                    print(
                                        f"Download failed. Retrying in {wait_time:.2f} seconds..."
                                    )
                                    time.sleep(wait_time)
                                else:
                                    print(
                                        f"Failed to download PDF for {paper_id} after {max_retries} attempts: {e}"
                                    )
                    except Exception as e:
                        print(f"Error downloading PDF for {paper_id}: {e}")
                else:
                    print(f"PDF link not found for entry: {title}")
            except Exception as e:
                print(f"Error processing entry: {e}")
                continue

    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
    except Exception as e:
        print(f"Unexpected error in download_pdfs: {e}")

    return downloaded_ids


def extract_arxiv_metadata(paper_id: str, output_folder: str) -> bool:
    """
    Extract metadata from an Arxiv paper and save it as a JSON file.
    Returns True if successful, False otherwise.

    Args:
        paper_id (str): The Arxiv paper ID (e.g., "2402.01359v2").
        output_folder (str): The path to the folder where the JSON file will be saved.

    Returns:
        bool: Whether metadata was successfully extracted and saved
    """
    try:
        # 1. Get the data from the Arxiv API
        url = f'http://export.arxiv.org/api/query?id_list={paper_id}'

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(url) as response:
                    xml_data = response.read().decode('utf-8')
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (2**attempt) + random.uniform(0, 1)
                    print(
                        f"API request failed for metadata. Retrying in {wait_time:.2f} seconds..."
                    )
                    time.sleep(wait_time)
                else:
                    print(
                        f"Failed to get metadata after {max_retries} attempts: {e}"
                    )
                    return False

        # 2. Parse the XML
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom',
            'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
        }

        root = ET.fromstring(xml_data)
        entry = root.find('.//atom:entry', namespaces)

        if entry is None:
            print(f"No entry found for paper ID: {paper_id}")
            return False

        # 3. Extract the required fields
        title_elem = entry.find('./atom:title', namespaces)
        title = title_elem.text.strip(
        ) if title_elem is not None and title_elem.text else ""

        # Extract authors
        authors = []
        for author in entry.findall('./atom:author', namespaces):
            name_elem = author.find('./atom:name', namespaces)
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text)

        # Extract categories
        categories = []
        for category in entry.findall('./atom:category', namespaces):
            category_term = category.get('term')
            if category_term:
                categories.append(category_term)

        # Extract abstract
        abstract_elem = entry.find('./atom:summary', namespaces)
        abstract = abstract_elem.text.strip(
        ) if abstract_elem is not None and abstract_elem.text else ""

        # Extract datetime information
        updated_elem = entry.find('./atom:updated', namespaces)
        updated = updated_elem.text if updated_elem is not None and updated_elem.text else ""

        published_elem = entry.find('./atom:published', namespaces)
        published = published_elem.text if published_elem is not None and published_elem.text else ""

        # 4. Create the JSON dictionary in the specified order
        metadata = {
            'id': paper_id,
            'title': title,
            'authors': authors,
            'categories': categories,
            'abstract': abstract,
            'updated': updated,
            'published': published
        }

        # 5. Save the JSON dictionary to a file
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"{paper_id}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error extracting metadata for {paper_id}: {e}")
        return False


def main(output_folder: str,
         existing_ids: Set[str],
         target_pdfs_per_category: int = 125) -> None:
    """
    Interact with the arxiv API to download PDFs based on categories.
    
    Args:
        output_folder (str): The folder to save PDFs and metadata to
        existing_ids (Set[str]): Set of paper IDs to avoid downloading
        target_pdfs_per_category (int): Number of PDFs to download for each category
    """
    try:
        arxiv_categories = read_yaml('configs/arxiv_configs.yaml')['categories']
    except Exception as e:
        print(f"Error reading config: {e}")
        raise ValueError("Failed to read arxiv categories")

    # Keep track of successfully downloaded PDFs for each category
    successful_downloads = {}

    # Create category directories first
    for category in arxiv_categories:
        pdf_dir = os.path.join(output_folder, 'pdf', category)
        os.makedirs(pdf_dir, exist_ok=True)
        # successful_downloads[category] = []
        successful_downloads[category] = [
            name.replace('.pdf', '')
            for name in os.listdir(pdf_dir)
            if name.endswith('.pdf')
        ]

    # Download PDFs for each category
    for category in arxiv_categories:
        print(f"\n--- Starting downloads for {category} ---")

        # Initialize counters and progress tracking
        pdfs_downloaded = 0
        results_offset = 0
        batch_size = 50  # How many results to fetch in each API call

        # Create a directory for this category
        pdf_dir = os.path.join(output_folder, 'pdf', category)

        # Continue fetching until we have enough PDFs for this category
        while pdfs_downloaded < target_pdfs_per_category:
            print(
                f"Category {category}: {pdfs_downloaded}/{target_pdfs_per_category} PDFs downloaded. Fetching more..."
            )

            # Iterate through subcategories, distributing the work
            total_subcategories = len(arxiv_categories[category])
            if total_subcategories == 0:
                print(f"No subcategories for {category}, skipping")
                break

            for sub_category in arxiv_categories[category]:
                if pdfs_downloaded >= target_pdfs_per_category:
                    break

                # Define metadata for query
                metadata = {
                    "cat": sub_category,
                    "submittedDate": "[202401010600+TO+202501010600]"
                }

                try:
                    # Get response from Arxiv API
                    response = get_response(metadata=metadata,
                                            max_results=batch_size,
                                            start=results_offset)

                    # Download PDFs from this response
                    new_ids = download_pdfs(
                        response=response,
                        download_dir=pdf_dir,
                        existing_ids=existing_ids,
                        target_count=target_pdfs_per_category,
                        current_count=pdfs_downloaded)

                    # Update counters
                    pdfs_downloaded += len(new_ids)
                    successful_downloads[category].extend(new_ids)

                    # Add new IDs to existing_ids to avoid duplication in future subcategories
                    existing_ids.update(new_ids)

                except Exception as e:
                    print(f"Error processing {category} {sub_category}: {e}")
                    # Continue with next subcategory instead of failing
                    continue

            # Increment offset for next batch of results
            results_offset += batch_size

            # Add a small delay to avoid hitting API rate limits
            time.sleep(1)

            # Break if we've gone too far without finding enough papers
            if results_offset > 1000:
                print(
                    f"Warning: Reached large offset ({results_offset}) for {category}. "
                    f"Only found {pdfs_downloaded}/{target_pdfs_per_category} PDFs."
                )
                break

    # Extract metadata for all downloaded PDFs
    print("\n--- Extracting metadata for all downloaded PDFs ---")
    metadata_folder = os.path.join(output_folder, 'metadata')
    os.makedirs(metadata_folder, exist_ok=True)

    total_metadata_success = 0
    total_metadata_failure = 0

    for category, paper_ids in successful_downloads.items():
        print(
            f"\nExtracting metadata for {len(paper_ids)} papers in {category}..."
        )
        success_count = 0

        for paper_id in tqdm(paper_ids):
            if os.path.exists(os.path.join(metadata_folder,
                                           f"{paper_id}.json")):
                print(f"Metadata already exists for {paper_id}, skipping")
                success_count += 1
                continue
            if extract_arxiv_metadata(paper_id, metadata_folder):
                success_count += 1
            else:
                total_metadata_failure += 1

        total_metadata_success += success_count
        print(
            f"Successfully extracted metadata for {success_count}/{len(paper_ids)} papers in {category}"
        )

    # Final summary
    print("\n--- Download Summary ---")
    total_papers = 0
    for category, paper_ids in successful_downloads.items():
        print(f"{category}: {len(paper_ids)} PDFs downloaded")
        total_papers += len(paper_ids)

    print(f"\nTotal PDFs downloaded: {total_papers}")
    print(f"Metadata extracted successfully: {total_metadata_success}")
    print(f"Metadata extraction failures: {total_metadata_failure}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download PDFs from arXiv")
    parser.add_argument(
        '--output_folder',
        type=str,
        default='data/raw/pdf/arxiv')
    parser.add_argument('--target_per_category',
                        type=int,
                        default=375,
                        help='Number of PDFs to download per category')
    args = parser.parse_args()

    # Create output directory
    output_folder = args.output_folder
    os.makedirs(output_folder, exist_ok=True)

    existing_ids = set([
        fname.replace('.json', '') for fname in os.listdir(
            'data/final/pdf/arxiv/corpus')
    ])

    main(output_folder, existing_ids, args.target_per_category)
