import re
import os
import json
from mistralai import Mistral
from typing import Any, Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential

class MistralOCR:
    """A class to handle OCR operations using Mistral and OpenAI APIs.

    This class provides methods to upload a PDF file to the Mistral API, extract OCR data,
    and convert the extracted data to Markdown format with embedded image data.
    """

    def __init__(self, mistral_api_key: str = None, openai_api_key: str = None) -> None:
        """Initializes the MistralOCR instance with API keys"""
        final_mistral_api_key = mistral_api_key or os.environ.get("MISTRAL_API_KEY")
        if not final_mistral_api_key:
            raise ValueError("Mistral API key is required. Please provide it via function argument or environment variable.")

        self.mistral_client = Mistral(api_key=final_mistral_api_key)

    def upload(self, path: str) -> None:
        """Uploads a PDF file to Mistral API"""
        self.uploaded_pdf = self.mistral_client.files.upload(
            file={
                "file_name": "uploaded_file.pdf",
                "content": open(path, "rb"),
            },
            purpose="ocr"
        )
        self.signed_url = self.mistral_client.files.get_signed_url(file_id=self.uploaded_pdf.id)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def extract(self):
        """Parse the OCR response from Mistral API"""
        response = self.mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": self.signed_url.url,
            },
            include_image_base64=True
        )
        return json.loads(response.model_dump_json())

    def get_raw_markdown(self, ocr_response) -> str:
        """Generates Markdown text and gathers image data from the OCR response.

        Iterates over the pages in the OCR response, collecting Markdown text and
        image data (base64 encoded) for each image.

        Args:
            ocr_response (dict): The OCR response containing pages and images.

        Returns:
            tuple: A tuple containing:
                - str: The concatenated Markdown text from all pages.
                - dict: A dictionary mapping image IDs to their base64 encoded image data.
        """
        markdowns: list[str] = []
        image_data = {}
        for page in ocr_response['pages']:
            for img in page['images']:
                image_data[img['id']] = img['image_base64']
            markdowns.append(page['markdown'])
        return "\n\n".join(markdowns), image_data

    def process_markdown(self, markdown_str, image_data_dict):
        """Processes the markdown string into a dictionary of data.

        Extracts all tables and replaces them in the text with placeholders.

        Returns:
            dict: A dictionary with 3 keys:
                - "text": the Markdown string with table blocks replaced by placeholders,
                - "tables": a dict mapping each table placeholder (e.g. "table_0") to its table string,
                - "images": identical to the input image data dictionary.
        """
        lines = markdown_str.splitlines()
        result_lines = []
        tables = {}
        i = 0
        table_count = 0

        while i < len(lines):
            line = lines[i]
            # Check if the current line looks like a table row and the next line is a separator row.
            if i < len(lines) - 1 and self._is_table_row(line) and self._is_separator_line(lines[i+1]):
                table_lines = [line, lines[i+1]]
                i += 2
                # Collect subsequent table rows.
                while i < len(lines) and self._is_table_row(lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                table_str = "\n".join(table_lines)
                table_id = f"table_{table_count}"
                # Replace the table block with a placeholder in the same style as images.
                result_lines.append(f"![{table_id}]({table_id})")
                tables[table_id] = table_str
                table_count += 1
            else:
                result_lines.append(line)
                i += 1

        new_text = "\n".join(result_lines)
        return {"text": new_text, "tables": tables, "images": image_data_dict}

    def split_into_sections_with_title(self, processed_text):
        """
        Splits the processed markdown text into a title (if it exists) and a list of sections.

        Hierarchy rules:
            - If the text starts with a header, assume that the first header (and its succeeding non-header lines)
            is the title of the full document. This title is stored separately and is not included in the sections list.
            - When a section consists solely of header lines (i.e. no body text), that header is merged (prepended)
            to the next section that includes non-header content. If multiple such header-only sections occur consecutively,
            they are concatenated until a section with body text is encountered.
            - If the markdown text does not start with a header symbol, all text prior to the first header is ignored.
            - If a section's header (its first non-empty line) contains texts like "bibliography" or "reference" (case-insensitive),
            that section is omitted from the final output.

        Parameters:
            processed_text (str): The full processed markdown text (e.g. with table placeholders).

        Returns:
            dict: A dictionary with two keys:
                "title": The title string (empty if not found).
                "sections": A list of sections (strings) in order.
        """
        # Ignore text until the first header if it doesn't start with one.
        stripped_text = processed_text.lstrip()
        if not stripped_text.startswith('#'):
            header_match = re.search(r'(?m)^#+\s', processed_text)
            if header_match:
                processed_text = processed_text[header_match.start():]
            else:
                # No header found in the entire text.
                return {"title": "", "sections": []}

        # Split the text using a regex that looks ahead for header lines (one or more '#' followed by a space).
        sections = re.split(r'(?m)(?=^#+\s)', processed_text)
        sections = [s.strip() for s in sections if s.strip()]

        title = ""
        # If the first section starts with a header, treat it as the title.
        if sections and sections[0].lstrip().startswith('#'):
            title = sections[0]
            sections = sections[1:]

        # Merge sections that consist only of header lines with the next section that contains non-header content.
        merged_sections = []
        pending = ""  # holds concatenated header-only sections
        for sec in sections:
            if self.is_only_headers(sec):
                pending = pending + "\n" + sec if pending else sec
            else:
                if pending:
                    sec = pending + "\n" + sec
                    pending = ""
                merged_sections.append(sec)
        if pending:
            merged_sections.append(pending)

        # Filter out sections whose first header line contains "bibliography" or "reference" (case-insensitive).
        filtered_sections = []
        for sec in merged_sections:
            # Find the first non-empty line in the section.
            for line in sec.splitlines():
                stripped_line = line.strip()
                if stripped_line:
                    header_line = stripped_line
                    break
            else:
                header_line = ""
            # Check if the header line contains "bibliograph" or "reference".
            if header_line.lower().find("bibliograph") != -1 or header_line.lower().find("reference") != -1:
                continue
            filtered_sections.append(sec)

        return {"title": title, "sections": filtered_sections}

    @staticmethod
    def _is_table_row(line):
        """Returns True if the line appears to be a Markdown table row."""
        stripped = line.strip()
        return '|' in stripped and stripped.startswith('|') and stripped.endswith('|')

    @staticmethod
    def _is_separator_line(line):
        """Returns True if the line is a table separator line. For example, valid cells: '---', ':--', '--:', or ':--:'."""
        stripped = line.strip()
        if not (stripped.startswith('|') and stripped.endswith('|')):
            return False
        # Remove the starting and ending pipes and split by pipe.
        cells = stripped[1:-1].split('|')
        for cell in cells:
            cell = cell.strip()
            # Adjust regex to accept at least 2 dashes.
            if not re.match(r'^:?-{1,}:?$', cell):
                return False
        return True

    @staticmethod
    def is_only_headers(section):
        """
        Returns True if every non-empty line in the section starts with '#' (i.e. the section contains only header lines).
        """
        lines = section.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.lstrip().startswith('#'):
                return False
        return True

    @staticmethod
    def _replace_placeholders_in_markdown(markdown_str: str, placeholder_dict: dict) -> str:
        """Replaces placeholders in Markdown with actual table string or base64 encoded image data.

        Args:
            markdown_str (str): The Markdown text containing image placeholders.
            images_dict (dict): A dictionary mapping image names to base64 encoded strings.

        Returns:
            str: The Markdown text with images replaced by base64 data.
        """
        for placeholder, content in placeholder_dict.items():
            markdown_str = markdown_str.replace(f"![{placeholder}]({placeholder})", f"![{placeholder}]({content})")
        return markdown_str

    def convert_pdf_to_markdown(self, path: str) -> str:
        """Converts a PDF file to Markdown using OCR.

        Args:
            path (str): The file path of the PDF to be converted.

        Returns:
            str: The Markdown text extracted from the PDF.
        """
        self.upload(path)
        ocr_response = self.extract()
        markdown, image_data = self.get_raw_markdown(ocr_response)
        self.markdown = self.process_markdown(markdown, image_data)
        return self.markdown