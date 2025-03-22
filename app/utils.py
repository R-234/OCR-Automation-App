# import os
# import shutil
# from zipfile import ZipFile
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# def create_zip(folder, zip_name):
#     """Create a ZIP file of all images in a folder."""
#     try:
#         zip_path = zip_name
#         with ZipFile(zip_path, 'w') as zipf:
#             for file in os.listdir(folder):
#                 file_path = os.path.join(folder, file)
#                 zipf.write(file_path, arcname=file)
#         return zip_path
#     except Exception as e:
#         logging.error(f"Error creating ZIP file: {e}")
#         return None

# def cleanup_folders(*folders):
#     """Delete all files in the specified folders."""
#     try:
#         for folder in folders:
#             for file in os.listdir(folder):
#                 file_path = os.path.join(folder, file)
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#                 elif os.path.isdir(file_path):
#                     shutil.rmtree(file_path)
#             logging.info(f"Cleaned up folder: {folder}")
#     except Exception as e:
#         logging.error(f"Error cleaning up folders: {e}")

import os
import shutil
import logging

def create_zip(folder_path, zip_name):
    """Create a ZIP file from the contents of a folder."""
    try:
        shutil.make_archive(zip_name, 'zip', folder_path)
        zip_path = f"{zip_name}.zip"
        logging.info(f"Created ZIP file: {zip_path}")
        return zip_path
    except Exception as e:
        logging.error(f"Error creating ZIP file: {e}")
        return None

def cleanup_folders(*folders):
    """Clean up the contents of the specified folders."""
    for folder in folders:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logging.error(f"Error deleting {file_path}: {e}")