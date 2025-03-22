
# import os

# # Define base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Define data directories
# IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "upload_images")
# OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "renamed_images")
# FAILED_FOLDER = os.path.join(BASE_DIR, "data", "failed_images")
# DEBUG_FOLDER = os.path.join(BASE_DIR, "data", "debug_images")

# # Define ZIP file paths
# ZIP_SUCCESS = os.path.join(BASE_DIR, "data", "processed_results.zip")
# ZIP_FAILED = os.path.join(BASE_DIR, "data", "failed_results.zip")

# # Ensure directories exist
# for folder in [IMAGE_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, DEBUG_FOLDER]:
#     os.makedirs(folder, exist_ok=True)





import os

# Folder paths
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")
FAILED_FOLDER = os.path.join(os.getcwd(), "failed")
DEBUG_FOLDER = os.path.join(os.getcwd(), "debug")

# ZIP file names
ZIP_SUCCESS = "renamed_images.zip"
ZIP_FAILED = "failed_images.zip"

# Fixed bounding box coordinates (x, y, width, height)
ID_BOX_COORDINATES = (120, 131, 275, 160)  # Replace with your actual coordinates