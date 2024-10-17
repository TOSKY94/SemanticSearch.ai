from unittest import mock
from unittest.mock import MagicMock, patch
from app.services.pdf_utils import PDFUtils

@patch('fitz.open')
def test_extract_text_from_pdf_success(mock_open):
    # Mock the PDF document object
    mock_doc = MagicMock()
    mock_open.return_value = mock_doc

    # Mock the page object
    mock_page = MagicMock()
    mock_page.get_text.return_value = "This is some text on page 1"
    mock_doc.load_page.return_value = mock_page

    # Mock the page count
    mock_doc.page_count = 2

    # Create an instance of the PDFUtils class
    pdf_utils = PDFUtils()

    # Call the method
    pdf_path = "path/to/pdf.pdf"
    extracted_text = pdf_utils.extract_text_from_pdf(pdf_path)

    # Assert the results
    assert extracted_text == "This is some text on page 1This is some text on page 1"
    mock_open.assert_called_once_with(pdf_path)
    mock_doc.load_page.assert_called()
    mock_page.get_text.assert_called()

@patch('fitz.open')
def test_extract_text_from_pdf_error(mock_open):
    # Mock an error when opening the PDF document
    mock_open.side_effect = Exception("Error opening PDF")

    # Create an instance of the PDFUtils class
    pdf_utils = PDFUtils()

    # Call the method
    pdf_path = "path/to/pdf.pdf"
    with mock.patch('builtins.open', side_effect=Exception("Error opening PDF")):
        with mock.patch('sys.stdout') as mock_stdout:
            try:
                pdf_utils.extract_text_from_pdf(pdf_path)
            except Exception as e:
                assert str(e) == "Error extracting text from PDF"
    mock_open.assert_called_once_with(pdf_path)

@patch('fitz.open')
def test_extract_text_from_pdf_empty_text(mock_open):
    # Mock an empty text extraction
    mock_doc = MagicMock()
    mock_open.return_value = mock_doc
    mock_page = MagicMock()
    mock_page.get_text.return_value = ""
    mock_doc.load_page.return_value = mock_page
    mock_doc.page_count = 1

    # Create an instance of the PDFUtils class
    pdf_utils = PDFUtils()

    # Call the method
    pdf_path = "path/to/pdf.pdf"
    extracted_text = pdf_utils.extract_text_from_pdf(pdf_path)

    # Assert the results
    assert extracted_text == ""
    mock_open.assert_called_once_with(pdf_path)
    mock_doc.load_page.assert_called_once()
    mock_page.get_text.assert_called_once()