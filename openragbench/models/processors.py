import re
import os
import json
from mistralai import Mistral
from tenacity import retry, stop_after_attempt, wait_random_exponential


class MarkdownProcessor:
    """A class to handle Markdown processing operations.

    This class provides methods to process Markdown text, including handling tables
    and images, and splitting the text into sections.
    """

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
            if i < len(lines) - 1 and self._is_table_row(
                    line) and self._is_separator_line(lines[i + 1]):
                table_lines = [line, lines[i + 1]]
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

    def split_sections(self, processed_markdown):
        """
        Splits the processed markdown into a title (if it exists) and a list of sections.
        Each section is a dictionary with its own text, tables, and images.

        Args:
            processed_markdown (dict): The processed markdown dictionary with 'text', 'tables', and 'images' keys.

        Returns:
            dict: A dictionary with two keys:
                "title": The title string (empty if not found).
                "sections": A list of section dictionaries, each with 'text', 'tables', and 'images' keys.
        """
        processed_text = processed_markdown["text"]
        all_tables = processed_markdown["tables"]
        all_images = processed_markdown["images"]

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
            if self._is_only_headers(sec):
                pending = pending + "\n" + sec if pending else sec
            else:
                if pending:
                    sec = pending + "\n" + sec
                    pending = ""
                merged_sections.append(sec)
        if pending:
            merged_sections.append(pending)

        # Filter out sections whose first header line contains "bibliography" or "reference" (case-insensitive).
        section_dicts = []
        for sec in merged_sections:
            # Extract tables and images referenced in this section
            section_tables = {}
            section_images = {}

            # Find all markdown image-like placeholders in this section
            placeholders = re.findall(r'!\[(.*?)\]\((.*?)\)', sec)
            for alt_text, url in placeholders:
                # Strip whitespace for more flexible matching
                alt_text_stripped = alt_text.strip()
                url_stripped = url.strip()

                # Check if alt text and URL are identical (the placeholder format)
                if alt_text_stripped == url_stripped:
                    if url_stripped in all_tables:
                        section_tables[url_stripped] = all_tables[url_stripped]
                    elif url_stripped in all_images:
                        section_images[url_stripped] = all_images[url_stripped]

            # Create a section dictionary with text, tables, and images
            section_dict = {
                "text": sec,
                "tables": section_tables,
                "images": section_images
            }
            section_dicts.append(section_dict)

        return {"title": title, "sections": section_dicts}

    def sections_to_doc(self, data):
        """
        Concatenate title and all section texts from the JSON document data,
        replacing any table placeholders with their actual content.

        Args:
            data (dict): Dictionary containing parsed JSON data with 'title' and 'sections'
            replace_placeholders_func (callable): Function to replace placeholders with content

        Returns:
            str: Concatenated string with title and all section texts separated by newlines
        """
        # Start with the title
        result = data["title"]

        # Add each section's text with a newline separator
        for section in data["sections"]:
            section_text = self.convert_section_to_chunk_text(section)
            result += "\n" + section_text
        return result

    def convert_section_to_chunk_text(self, section):
        section_text = section["text"]

        if section["tables"]:
            section_text = self.replace_placeholders(section_text,
                                                     section["tables"])

        if section["images"]:
            section_text = self.delete_placeholders(section_text,
                                                    section["images"])

        return section_text

    def replace_placeholders(self, markdown_str: str,
                             placeholder_dict: dict) -> str:
        """Replaces placeholders in Markdown with actual table string or base64 encoded image data.

        Args:
            markdown_str (str): The Markdown text containing image placeholders.
            placeholder_dict (dict): A dictionary mapping placeholders to their content.

        Returns:
            str: The Markdown text with placeholders replaced by their content.
        """
        for placeholder, content in placeholder_dict.items():
            markdown_str = markdown_str.replace(
                f"![{placeholder}]({placeholder})", content)
        return markdown_str

    def delete_placeholders(self, markdown_str: str,
                            placeholder_dict: dict) -> str:
        """Deletes placeholders in Markdown.

        Args:
            markdown_str (str): The Markdown text containing image placeholders.
            placeholder_dict (dict): A dictionary mapping placeholders to their content.

        Returns:
            str: The Markdown text with placeholders deleted.
        """
        for placeholder in placeholder_dict.keys():
            markdown_str = markdown_str.replace(
                f"![{placeholder}]({placeholder})", "")
        return markdown_str

    def concat_section_with_qa_pairs(self, sections, qa_pairs):
        """
        Integrates QA pairs with each section in the markdown document.

        Args:
            sections (dict): A dictionary with "title" and "sections" keys,
                             where each section is a dictionary with "text", "tables", and "images" keys.
            qa_pairs (list): A list of lists, where each inner list contains QA pairs for the corresponding section.

        Returns:
            dict: An integrated dictionary with "title" and "sections" keys,
                  where each section has "text", "tables", "images", and "qa_pairs" keys.
        """
        if len(sections["sections"]) != len(qa_pairs):
            raise ValueError(
                "Mismatch between number of sections and QA pair lists")

        integrated_data = {"title": sections["title"], "sections": []}

        for i, section in enumerate(sections["sections"]):
            # Create a copy of the section dictionary and add the QA pairs
            section_data = section.copy(
            )  # This preserves "text", "tables", and "images"
            section_data["qa_pairs"] = qa_pairs[i]
            integrated_data["sections"].append(section_data)

        return integrated_data

    @staticmethod
    def _is_table_row(line):
        """Returns True if the line appears to be a Markdown table row."""
        stripped = line.strip()
        return '|' in stripped and stripped.startswith(
            '|') and stripped.endswith('|')

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
    def _is_only_headers(section):
        """Returns True if every non-empty line in the section starts with '#' (i.e. header)."""
        lines = section.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.lstrip().startswith('#'):
                return False
        return True

    @staticmethod
    def has_tables(markdown_text):
        """
        Checks if the markdown text contains table placeholders.

        Args:
            markdown_text (str): The markdown text to check.

        Returns:
            bool: True if the text contains table placeholders, False otherwise.
        """
        # Look for table placeholders in the format ![table_N](table_N)
        table_pattern = r'!\[(table_\d+)\]\((table_\d+)\)'
        return bool(re.search(table_pattern, markdown_text))

    @staticmethod
    def has_images(markdown_text):
        """
        Checks if the markdown text contains image placeholders.

        Args:
            markdown_text (str): The markdown text to check.

        Returns:
            bool: True if the text contains image placeholders, False otherwise.
        """
        # First, identify all table placeholders to exclude them
        table_pattern = r'!\[(table_\d+)\]\((table_\d+)\)'
        table_matches = re.findall(table_pattern, markdown_text)

        # Create a temporary text with table placeholders removed
        temp_text = markdown_text
        for match in table_matches:
            table_id = match[0]  # They should be the same in both positions
            temp_text = temp_text.replace(f"![{table_id}]({table_id})", "")

        # Now check for any remaining image patterns
        image_pattern = r'!\[([^]]+)\]\(([^)]+)\)'
        return bool(re.search(image_pattern, temp_text))


class MistralOCR:
    """A class to handle OCR operations using Mistral API.

    This class provides methods to upload a PDF file to the Mistral API, extract OCR data,
    and convert the extracted data to Markdown format with embedded image data.
    """

    def __init__(self, mistral_api_key: str = None) -> None:
        """Initializes the MistralOCR instance with API keys"""
        final_mistral_api_key = mistral_api_key or os.environ.get(
            "MISTRAL_API_KEY")
        if not final_mistral_api_key:
            raise ValueError(
                "Mistral API key is required. Please provide it via function argument or environment variable."
            )

        self.mistral_client = Mistral(api_key=final_mistral_api_key)
        self.markdown_processor = MarkdownProcessor()

    def upload(self, path: str) -> None:
        """Uploads a PDF file to Mistral API"""
        self.uploaded_pdf = self.mistral_client.files.upload(file={
            "file_name": "uploaded_file.pdf",
            "content": open(path, "rb"),
        },
                                                             purpose="ocr")
        self.signed_url = self.mistral_client.files.get_signed_url(
            file_id=self.uploaded_pdf.id)

    @retry(wait=wait_random_exponential(min=1, max=60),
           stop=stop_after_attempt(6))
    def extract(self):
        """Parse the OCR response from Mistral API"""
        response = self.mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": self.signed_url.url,
            },
            include_image_base64=True)
        return json.loads(response.model_dump_json())

    def get_raw_markdown(self, ocr_response):
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
        markdowns = []
        image_data = {}
        for page in ocr_response['pages']:
            for img in page['images']:
                image_data[img['id']] = img['image_base64']
            markdowns.append(page['markdown'])
        return "\n\n".join(markdowns), image_data

    def convert_pdf_to_markdown(self, path: str) -> dict:
        """Converts a PDF file to Markdown using OCR.

        Args:
            path (str): The file path of the PDF to be converted.

        Returns:
            dict: A dictionary containing the processed markdown data.
        """
        self.upload(path)
        ocr_response = self.extract()
        markdown, image_data = self.get_raw_markdown(ocr_response)
        self.markdown = self.markdown_processor.process_markdown(
            markdown, image_data)
        return self.markdown
