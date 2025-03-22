# import os
# import cv2
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# def rename_image(image, extracted_number, output_folder):
#     """Rename and save the image based on the extracted number."""
#     try:
#         # Create new filename
#         new_filename = f"{extracted_number}.jpg"
#         output_path = os.path.join(output_folder, new_filename)
        
#         # Save the image
#         success = cv2.imwrite(output_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
#         if not success:
#             raise ValueError("Failed to save image")
        
#         return new_filename
#     except Exception as e:
#         logging.error(f"Error renaming image: {e}")
#         return None
    

import os
import cv2
import logging

def rename_image(image, extracted_number, output_folder):
    """Rename and save the image with the extracted number."""
    try:
        new_filename = f"{extracted_number}.jpg"
        new_filepath = os.path.join(output_folder, new_filename)
        
        # Save the image
        cv2.imwrite(new_filepath, image)
        
        logging.info(f"Renamed image saved: {new_filepath}")
        return new_filename
    except Exception as e:
        logging.error(f"Error renaming image: {e}")
        return None