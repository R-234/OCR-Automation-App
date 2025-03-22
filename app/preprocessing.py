# import cv2
# import numpy as np
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# def preprocess_image(image):
#     """High-quality preprocessing: grayscale, noise reduction, adaptive thresholding."""
#     try:
#         # Convert to grayscale
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Apply Non-Local Means Denoising
#         denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
        
#         # Apply CLAHE for contrast enhancement
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#         enhanced = clahe.apply(denoised)
        
#         # Apply Median Blur for noise reduction
#         blurred = cv2.medianBlur(enhanced, 5)
        
#         # Apply Adaptive Thresholding
#         thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
#         # Apply Morphological Transformations to remove small noise
#         kernel = np.ones((3, 3), np.uint8)
#         clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
#         return clean
#     except Exception as e:
#         logging.error(f"Error in preprocessing: {e}")
#         return None
    















import cv2
import logging

def preprocess_image(image):
    """Preprocess the image for OCR."""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        return thresh
    except Exception as e:
        logging.error(f"Error during preprocessing: {e}")
        return None

def crop_id_region(image, x, y, w, h):
    """Crop the image to the specified bounding box."""
    try:
        cropped_image = image[y:y+h, x:x+w]
        return cropped_image
    except Exception as e:
        logging.error(f"Error cropping image: {e}")
        return None 