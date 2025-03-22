import pytesseract
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def extract_text(image):
    """Extract numbers using Tesseract OCR with custom configurations."""
    try:
        # Use Tesseract with custom configurations
        custom_config = r'--psm 11 --oem 1 -l eng'  # PSM 11: Sparse text
        extracted_text = pytesseract.image_to_string(image, config=custom_config).strip()
        
        # Extract only numeric characters
        numbers_only = re.sub(r'\D', '', extracted_text)
        
        logging.info(f"Extracted text: {extracted_text}")
        logging.info(f"Numbers only: {numbers_only}")
        
        return numbers_only
    except Exception as e:
        logging.error(f"Error in text extraction: {e}")
        return None