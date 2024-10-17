import fitz
import re

class PDFUtils:
    def __init__(self):
        pass

    def clean_text(self, text):
        """Cleans up extracted PDF text by replacing newlines, removing bullets and irregular characters."""
        # Replace newlines with spaces
        cleaned_text = text.replace("\n", " ")

        # Remove common bullet characters (e.g., •, -, *, →, etc.)
        cleaned_text = re.sub(r"[•\-\*\→]", "", cleaned_text)

        # Remove any other unwanted irregular characters (non-ASCII)
        cleaned_text = re.sub(r"[^\x00-\x7F]+", " ", cleaned_text)

        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

        return cleaned_text

    def extract_text_from_pdf(self, pdf_path):
        """Extracts and cleans text from a PDF file."""
        try:
            pdf_document = fitz.open(pdf_path)
            extracted_text = ""

            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                extracted_text += page.get_text()

            pdf_document.close()

            # Clean up the extracted text
            cleaned_text = self.clean_text(extracted_text)
            return cleaned_text

        except Exception as e:
            raise Exception("Error extracting text from PDF")
