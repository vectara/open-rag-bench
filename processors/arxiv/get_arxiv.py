import os
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict

def read_json(path: str) -> Dict:
    """Read JSON from a file."""
    with open(path, 'r') as f:
        return json.load(f)

def get_response(query: str | None = None,
                 metadata: Dict[str, str] = {},
                 max_results: int = 10) -> str:
    """
    Retrieve an API response from arxiv based on a search query and metadata.

    Args:
        query (Optional[str]): The search query. If provided, it will be URL-encoded
                               and added to the metadata.
        metadata (Dict[str, str]): A dictionary of metadata parameters for the query.
        max_results (int): The maximum number of results to fetch.

    Returns:
        str: The response data decoded as a UTF-8 string.
    """
    if query is not None:
        metadata['all'] = urllib.parse.quote(query)
    combined_query = '+AND+'.join([f'{k}:{v}' for k, v in metadata.items()])
    url = (f'http://export.arxiv.org/api/query?search_query={combined_query}'
           f'&start=0&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending')
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def download_pdfs(response: str, download_dir: str = 'data/pdf/arxiv') -> None:
    """
    Parse an arxiv API response and download the corresponding PDFs.

    Args:
        response (str): The XML response from the arxiv API.
        download_dir (str): The directory where downloaded PDFs will be saved.

    Raises:
        ET.ParseError: If the response cannot be parsed as valid XML.
    """
    os.makedirs(download_dir, exist_ok=True)

    root = ET.fromstring(response)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ').replace(' ', '_')
        pdf_url = None

        for link in entry.findall('atom:link', ns):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib['href']
                break

        if pdf_url:
            file_name = pdf_url.split('/')[-1] + '.pdf'
            file_path = os.path.join(download_dir, file_name)
            if os.path.exists(file_path):
                print(f"PDF already exists for entry:", title)
                continue
            print(f"Downloading {pdf_url} to {file_path}")
            urllib.request.urlretrieve(pdf_url, file_path)
        else:
            print("PDF link not found for entry:", title)

def main():
    """Interact with the arxiv API to download PDFs based on categories."""
    try:
        arxiv_categories = read_json('../configs/arxiv_categories.json')
    except:
        raise ValueError("Failed to read arxiv categories")

    for category in arxiv_categories:
        print(f"Downloading {category}...")

        total_categories = len(arxiv_categories[category])
        if total_categories == 0:
            continue
        max_results = 50 // total_categories
        residual = 50 % total_categories

        for i, sub_category in enumerate(arxiv_categories[category]):
            metadata = {
                "cat": sub_category,
                "submittedDate": "[202401010600+TO+202501010600]"
            }
            curr_max_results = max_results + 1 if i < residual else max_results
            try:
                response = get_response(metadata=metadata, max_results=curr_max_results)
                download_pdfs(response, download_dir=f'pdf/arxiv/{category}')
            except Exception as e:
                print(f"Failed to download {category} {sub_category}: {e}")
                raise ValueError("Failed to download") from e


if __name__ == "__main__":
    main()