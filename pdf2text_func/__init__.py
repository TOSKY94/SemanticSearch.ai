import azure.functions as func
from app.services.pdf_utils import PDFUtils
from app.models.models import Response
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def main(req: func.HttpRequest) -> func.HttpResponse:
    pdf_path = None  # Declare pdf_path to ensure it's available in the finally block
    
    try:
        logging.info('processing pdf to text')

        # Get the file from the request
        uploaded_file = req.files['file']

        # Check if it's a valid PDF file
        if uploaded_file.filename == '' or not uploaded_file.filename.endswith('.pdf'):
            response_model = Response(
                status="error",
                message="Invalid file type",
                error="Invalid file type. Only PDF is allowed."
            )
            return func.HttpResponse(response_model.to_json(), status_code=400, mimetype='application/json')


        # Use a temporary directory (recommended for Azure Functions)
        temp_dir = '/tmp' if os.name != 'nt' else os.getcwd()
        
        # Save the uploaded PDF file to the temporary location
        pdf_path = os.path.join(temp_dir, uploaded_file.filename)
        with open(pdf_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Extract text from the PDF
        extracted_text = PDFUtils().extract_text_from_pdf(pdf_path)

        response_model = Response(
            status="success",
            message="Text extracted successfully",
            data={"extracted_text": extracted_text}
        )

        return func.HttpResponse(response_model.to_json(),
                                 status_code=200, mimetype='application/json')

    except Exception as e:
        logging.error(f"Error in pdf2text functionality: {str(e)}")
        response_model = Response(
            status="error",
            message="PDF processing failed",
            error=str(e)
        )
        return func.HttpResponse(response_model.to_json(), status_code=500, mimetype='application/json')

    finally:
        # Remove the PDF file after processing
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                logging.info(f"Temporary file {pdf_path} has been removed.")
            except Exception as e:
                logging.error(f"Error removing temporary file {pdf_path}: {str(e)}")
