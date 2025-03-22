# import streamlit as st
# import cv2
# import logging
# import os
# import shutil
# import concurrent.futures
# import numpy as np
# import re
# from PIL import Image
# from config import IMAGE_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, ZIP_SUCCESS, ZIP_FAILED, DEBUG_FOLDER
# from utils import create_zip, cleanup_folders
# from preprocessing import preprocess_image
# from ocr import extract_text
# from rename_images import rename_image

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Ensure folders exist
# os.makedirs(IMAGE_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(FAILED_FOLDER, exist_ok=True)
# os.makedirs(DEBUG_FOLDER, exist_ok=True)

# def process_single_image(image_file):
#     """Process a single image and return the result."""
#     try:
#         image_path = os.path.join(IMAGE_FOLDER, image_file)
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError(f"Error loading image: {image_file}")
        
#         # Preprocess the image
#         processed_image = preprocess_image(image)
#         if processed_image is None:
#             raise ValueError("Image preprocessing failed")
        
#         # Extract text using Tesseract
#         extracted_number = extract_text(processed_image)
#         if not extracted_number:
#             raise ValueError("Text extraction failed")
        
#         # Validate extracted number (must be 4 or 5 digits)
#         if len(extracted_number) < 4 or len(extracted_number) > 5:
#             raise ValueError(f"Invalid number length: {extracted_number}")
        
#         # Rename and save the image
#         new_filename = rename_image(image, extracted_number, OUTPUT_FOLDER)
#         if not new_filename:
#             raise ValueError("Failed to rename image")
        
#         return None, new_filename  # Success: No failed file, return new filename
#     except Exception as e:
#         logging.error(f"Error processing {image_file}: {e}")
#         return image_file, None  # Failure: Return failed file, no new filename

# def process_images_parallel(image_files):
#     """Process multiple images using multi-threading."""
#     renamed_files, failed_files = [], []
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Limit threads
#         results = executor.map(process_single_image, image_files)

#     for failed, renamed in results:
#         if failed:
#             failed_files.append(failed)
#             src_path = os.path.join(IMAGE_FOLDER, failed)
#             dst_path = os.path.join(FAILED_FOLDER, failed)
            
#             # Check if the source file exists before moving
#             if os.path.exists(src_path):
#                 shutil.move(src_path, dst_path)
#             else:
#                 logging.error(f"File not found: {src_path}")
#         if renamed:
#             renamed_files.append(renamed)

#     return renamed_files, failed_files

# def process_and_zip(uploaded_files):
#     """Processes images using OCR and returns ZIP file paths."""
#     image_files = []
#     for file in uploaded_files:
#         if file.size > 5 * 1024 * 1024:  # 5MB limit
#             st.warning(f"Skipping {file.name} (too large).")
#             continue
        
#         file_path = os.path.join(IMAGE_FOLDER, file.name)
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         image_files.append(file.name)

#     renamed_files, failed_files = process_images_parallel(image_files)  # Use parallel processing

#     success_zip = create_zip(OUTPUT_FOLDER, ZIP_SUCCESS) if renamed_files else None
#     failed_zip = create_zip(FAILED_FOLDER, ZIP_FAILED) if failed_files else None

#     cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER)
#     return success_zip, failed_zip

# # Streamlit UI
# st.markdown(
#     """
#     <style>
#     @keyframes scrollText {
#         0% { transform: translateX(100%); }
#         100% { transform: translateX(-100%); }
#     }
#     .scrolling-text {
#         white-space: nowrap;
#         overflow: hidden;
#         position: relative;
#         width: 100%;
#         font-size: 20px;
#         font-weight: bold;
#         color: #0066cc;
#     }
#     .scrolling-text span {
#         display: inline-block;
#         animation: scrollText 10s linear infinite;
#     }
#     .title {
#         font-size: 30px;
#         font-weight: bold;
#         color: #ff5733;
#         text-align: center;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-size: 16px;
#         padding: 10px 24px;
#         border-radius: 8px;
#         border: none;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#     }
#     </style>
#     <div class='scrolling-text'><span>Blacklead Infratech PVT LTD</span></div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("<div class='title'>OCR Model for BIPL</div>", unsafe_allow_html=True)

# # File uploader with custom styling
# uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# # Process button with custom styling
# if st.button("Process Images", key="process_button"):
#     if uploaded_files:
#         # Clean up folders before processing
#         cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER, DEBUG_FOLDER)
        
#         with st.spinner("Processing images..."):
#             progress_bar = st.progress(0)
#             total_files = len(uploaded_files)
#             success_zip, failed_zip = process_and_zip(uploaded_files)
#             progress_bar.progress(1.0)  # Complete progress bar

#         st.success("Processing Completed!")

#         # Store ZIP file paths in session state
#         if success_zip:
#             st.session_state.success_zip = success_zip
#         if failed_zip:
#             st.session_state.failed_zip = failed_zip

# # Display download buttons if ZIP files exist in session state
# if "success_zip" in st.session_state or "failed_zip" in st.session_state:
#     col1, col2 = st.columns(2)

#     if "success_zip" in st.session_state:
#         with open(st.session_state.success_zip, "rb") as file:
#             col1.download_button(
#                 label="Download Processed Images (ZIP)",
#                 data=file,
#                 file_name=ZIP_SUCCESS,
#                 mime="application/zip"
#             )

#     if "failed_zip" in st.session_state:
#         with open(st.session_state.failed_zip, "rb") as file:
#             col2.download_button(
#                 label="Download Failed Images (ZIP)",
#                 data=file,
#                 file_name=ZIP_FAILED,
#                 mime="application/zip"
#             )
# else:
#     st.warning("Please upload images and click 'Process Images' to generate ZIP files.")








# import streamlit as st
# import cv2
# import logging
# import os
# import shutil
# import concurrent.futures
# import numpy as np
# import re
# from PIL import Image
# from config import IMAGE_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, ZIP_SUCCESS, ZIP_FAILED, DEBUG_FOLDER
# from utils import create_zip, cleanup_folders
# from preprocessing import preprocess_image
# from ocr import extract_text
# from rename_images import rename_image

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Ensure folders exist
# os.makedirs(IMAGE_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(FAILED_FOLDER, exist_ok=True)
# os.makedirs(DEBUG_FOLDER, exist_ok=True)

# def process_single_image(image_file):
#     """Process a single image and return the result."""
#     try:
#         image_path = os.path.join(IMAGE_FOLDER, image_file)
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError(f"Error loading image: {image_file}")
        
#         # Preprocess the image
#         processed_image = preprocess_image(image)
#         if processed_image is None:
#             raise ValueError("Image preprocessing failed")
        
#         # Extract text using Tesseract
#         extracted_number = extract_text(processed_image)
#         if not extracted_number:
#             raise ValueError("Text extraction failed")
        
#         # Validate extracted number (must be 4 or 5 digits)
#         if len(extracted_number) < 4 or len(extracted_number) > 5:
#             raise ValueError(f"Invalid number length: {extracted_number}")
        
#         # Rename and save the image
#         new_filename = rename_image(image, extracted_number, OUTPUT_FOLDER)
#         if not new_filename:
#             raise ValueError("Failed to rename image")
        
#         return None, new_filename  # Success: No failed file, return new filename
#     except Exception as e:
#         logging.error(f"Error processing {image_file}: {e}")
#         return image_file, None  # Failure: Return failed file, no new filename

# def process_images_parallel(image_files):
#     """Process multiple images using multi-threading."""
#     renamed_files, failed_files = [], []
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Limit threads
#         results = executor.map(process_single_image, image_files)

#     for failed, renamed in results:
#         if failed:
#             failed_files.append(failed)
#             src_path = os.path.join(IMAGE_FOLDER, failed)
#             dst_path = os.path.join(FAILED_FOLDER, failed)
            
#             # Check if the source file exists before moving
#             if os.path.exists(src_path):
#                 shutil.move(src_path, dst_path)
#             else:
#                 logging.error(f"File not found: {src_path}")
#         if renamed:
#             renamed_files.append(renamed)

#     return renamed_files, failed_files

# def process_and_zip(uploaded_files):
#     """Processes images using OCR and returns ZIP file paths."""
#     image_files = []
#     for file in uploaded_files:
#         if file.size > 5 * 1024 * 1024:  # 5MB limit
#             st.warning(f"Skipping {file.name} (too large).")
#             continue
        
#         file_path = os.path.join(IMAGE_FOLDER, file.name)
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         image_files.append(file.name)

#     renamed_files, failed_files = process_images_parallel(image_files)  # Use parallel processing

#     success_zip = create_zip(OUTPUT_FOLDER, "renamed_images.zip") if renamed_files else None
#     failed_zip = create_zip(FAILED_FOLDER, "failed_images.zip") if failed_files else None

#     cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER)
#     return success_zip, failed_zip

# # Streamlit UI
# st.markdown(
#     """
#     <style>
#     @keyframes scrollText {
#         0% { transform: translateX(100%); }
#         100% { transform: translateX(-100%); }
#     }
#     .scrolling-text {
#         white-space: nowrap;
#         overflow: hidden;
#         position: relative;
#         width: 100%;
#         font-size: 20px;
#         font-weight: bold;
#         color: #0066cc;
#     }
#     .scrolling-text span {
#         display: inline-block;
#         animation: scrollText 10s linear infinite;
#     }
#     .title {
#         font-size: 30px;
#         font-weight: bold;
#         color: #ff5733;
#         text-align: center;
#         font-family: 'Georgia', serif;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-size: 16px;
#         padding: 10px 24px;
#         border-radius: 8px;
#         border: none;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#     }
#     .developer-credit {
#         font-size: 14px;
#         text-align: center;
#         margin-top: 20px;
#         color: #555;
#     }
#     </style>
#     <div class='scrolling-text'><span>Blacklead Infratech PVT LTD</span></div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("<div class='title'>OCR Model for BIPL</div>", unsafe_allow_html=True)

# # File uploader with custom styling
# uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# # Process button with custom styling
# if st.button("Process Images", key="process_button"):
#     if uploaded_files:
#         # Clean up folders before processing
#         cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER, DEBUG_FOLDER)
        
#         with st.spinner("Processing images..."):
#             progress_bar = st.progress(0)
#             total_files = len(uploaded_files)
#             success_zip, failed_zip = process_and_zip(uploaded_files)
#             progress_bar.progress(1.0)  # Complete progress bar

#         st.success("Processing Completed!")

#         # Store ZIP file paths in session state
#         if success_zip:
#             st.session_state.success_zip = success_zip
#         if failed_zip:
#             st.session_state.failed_zip = failed_zip

# # Display download buttons if ZIP files exist in session state
# if "success_zip" in st.session_state or "failed_zip" in st.session_state:
#     col1, col2 = st.columns(2)

#     if "success_zip" in st.session_state:
#         with open(st.session_state.success_zip, "rb") as file:
#             col1.download_button(
#                 label="Download Processed Images (ZIP)",
#                 data=file,
#                 file_name="renamed_images.zip",
#                 mime="application/zip"
#             )

#     if "failed_zip" in st.session_state:
#         with open(st.session_state.failed_zip, "rb") as file:
#             col2.download_button(
#                 label="Download Failed Images (ZIP)",
#                 data=file,
#                 file_name="failed_images.zip",
#                 mime="application/zip"
#             )
# else:
#     st.warning("Please upload images and click 'Process Images' to generate ZIP files.")

# # Developer credit
# st.markdown("<div class='developer-credit'>Developed by Rakesh Rathaur</div>", unsafe_allow_html=True)
















































# import streamlit as st
# import cv2
# import logging
# import os
# import shutil
# import concurrent.futures
# from config import IMAGE_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, ZIP_SUCCESS, ZIP_FAILED, DEBUG_FOLDER
# from utils import create_zip, cleanup_folders
# from preprocessing import preprocess_image
# from ocr import extract_text
# from rename_images import rename_image

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Ensure folders exist
# os.makedirs(IMAGE_FOLDER, exist_ok=True)
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# os.makedirs(FAILED_FOLDER, exist_ok=True)
# os.makedirs(DEBUG_FOLDER, exist_ok=True)

# def process_single_image(image_file):
#     """Process a single image and return the result."""
#     try:
#         image_path = os.path.join(IMAGE_FOLDER, image_file)
#         image = cv2.imread(image_path)
#         if image is None:
#             raise ValueError(f"Error loading image: {image_file}")
        
#         # Preprocess the image
#         processed_image = preprocess_image(image)
#         if processed_image is None:
#             raise ValueError("Image preprocessing failed")
        
#         # Extract text using Tesseract
#         extracted_number = extract_text(processed_image)
#         if not extracted_number:
#             raise ValueError("Text extraction failed")
        
#         # Validate extracted number (must be 4 or 5 digits)
#         if len(extracted_number) < 4 or len(extracted_number) > 5:
#             raise ValueError(f"Invalid number length: {extracted_number}")
        
#         # Rename and save the image
#         new_filename = rename_image(image, extracted_number, OUTPUT_FOLDER)
#         if not new_filename:
#             raise ValueError("Failed to rename image")
        
#         logging.info(f"Successfully processed and renamed {image_file} to {new_filename}")
#         return None, new_filename  # Success: No failed file, return new filename
#     except Exception as e:
#         logging.error(f"Error processing {image_file}: {e}")
#         return image_file, None  # Failure: Return failed file, no new filename

# def process_images_parallel(image_files):
#     """Process multiple images using multi-threading."""
#     renamed_files, failed_files = [], []
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Limit threads
#         results = executor.map(process_single_image, image_files)

#     for failed, renamed in results:
#         if failed:
#             failed_files.append(failed)
#             src_path = os.path.join(IMAGE_FOLDER, failed)
#             dst_path = os.path.join(FAILED_FOLDER, failed)
            
#             # Check if the source file exists before moving
#             if os.path.exists(src_path):
#                 shutil.move(src_path, dst_path)
#             else:
#                 logging.error(f"File not found: {src_path}")
#         if renamed:
#             renamed_files.append(renamed)

#     return renamed_files, failed_files

# def process_and_zip(uploaded_files):
#     """Processes images using OCR and returns ZIP file paths."""
#     image_files = []
#     for file in uploaded_files:
#         if file.size > 5 * 1024 * 1024:  # 5MB limit
#             st.warning(f"Skipping {file.name} (too large).")
#             continue
        
#         file_path = os.path.join(IMAGE_FOLDER, file.name)
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         image_files.append(file.name)

#     renamed_files, failed_files = process_images_parallel(image_files)  # Use parallel processing

#     success_zip = create_zip(OUTPUT_FOLDER, ZIP_SUCCESS.replace(".zip", "")) if renamed_files else None
#     failed_zip = create_zip(FAILED_FOLDER, ZIP_FAILED.replace(".zip", "")) if failed_files else None

#     cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER)
#     return success_zip, failed_zip

# # Streamlit UI
# st.markdown(
#     """
#     <style>
#     @keyframes scrollText {
#         0% { transform: translateX(100%); }
#         100% { transform: translateX(-100%); }
#     }
#     .scrolling-text {
#         white-space: nowrap;
#         overflow: hidden;
#         position: relative;
#         width: 100%;
#         font-size: 20px;
#         font-weight: bold;
#         color: #0066cc;
#     }
#     .scrolling-text span {
#         display: inline-block;
#         animation: scrollText 10s linear infinite;
#     }
#     .title {
#         font-size: 30px;
#         font-weight: bold;
#         color: #ff5733;
#         text-align: center;
#         font-family: 'Georgia', serif;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         font-size: 16px;
#         padding: 10px 24px;
#         border-radius: 8px;
#         border: none;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#     }
#     .developer-credit {
#         font-size: 14px;
#         text-align: center;
#         margin-top: 20px;
#         color: #555;
#     }
#     </style>
#     <div class='scrolling-text'><span>Blacklead Infratech PVT LTD</span></div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("<div class='title'>OCR Model for BIPL</div>", unsafe_allow_html=True)

# # File uploader with custom styling
# uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# # Process button with custom styling
# if st.button("Process Images", key="process_button"):
#     if uploaded_files:
#         # Clean up folders before processing
#         cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER, DEBUG_FOLDER)
        
#         with st.spinner("Processing images..."):
#             progress_bar = st.progress(0)
#             total_files = len(uploaded_files)
#             success_zip, failed_zip = process_and_zip(uploaded_files)
#             progress_bar.progress(1.0)  # Complete progress bar

#         st.success("Processing Completed!")

#         # Store ZIP file paths in session state
#         if success_zip:
#             st.session_state.success_zip = success_zip
#         if failed_zip:
#             st.session_state.failed_zip = failed_zip

# # Display download buttons if ZIP files exist in session state
# if "success_zip" in st.session_state or "failed_zip" in st.session_state:
#     col1, col2 = st.columns(2)

#     if "success_zip" in st.session_state:
#         with open(st.session_state.success_zip, "rb") as file:
#             col1.download_button(
#                 label="Download Processed Images (ZIP)",
#                 data=file,
#                 file_name=ZIP_SUCCESS,
#                 mime="application/zip"
#             )

#     if "failed_zip" in st.session_state:
#         with open(st.session_state.failed_zip, "rb") as file:
#             col2.download_button(
#                 label="Download Failed Images (ZIP)",
#                 data=file,
#                 file_name=ZIP_FAILED,
#                 mime="application/zip"
#             )
# else:
#     st.warning("Please upload images and click 'Process Images' to generate ZIP files.")

# # Developer credit
# st.markdown("<div class='developer-credit'>Developed by Rakesh Rathaur</div>", unsafe_allow_html=True)


















































import streamlit as st
import cv2
import logging
import os
import shutil
import concurrent.futures
from config import IMAGE_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, ZIP_SUCCESS, ZIP_FAILED, DEBUG_FOLDER, ID_BOX_COORDINATES
from utils import create_zip, cleanup_folders
from preprocessing import preprocess_image, crop_id_region
from ocr import extract_text
from rename_images import rename_image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure folders exist
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(FAILED_FOLDER, exist_ok=True)
os.makedirs(DEBUG_FOLDER, exist_ok=True)

def process_single_image(image_file):
    """Process a single image and return the result."""
    try:
        image_path = os.path.join(IMAGE_FOLDER, image_file)
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Error loading image: {image_file}")
        
        # Crop the image to the ID region
        x, y, w, h = ID_BOX_COORDINATES
        cropped_image = crop_id_region(image, x, y, w, h)
        if cropped_image is None:
            raise ValueError("Failed to crop image to ID region")
        
        # Preprocess the cropped image
        processed_image = preprocess_image(cropped_image)
        if processed_image is None:
            raise ValueError("Image preprocessing failed")
        
        # Extract text using Tesseract
        extracted_number = extract_text(processed_image)
        if not extracted_number:
            raise ValueError("Text extraction failed")
        
        # Validate extracted number (must be 4 or 5 digits)
        if len(extracted_number) < 4 or len(extracted_number) > 5:
            raise ValueError(f"Invalid number length: {extracted_number}")
        
        # Rename and save the image
        new_filename = rename_image(image, extracted_number, OUTPUT_FOLDER)
        if not new_filename:
            raise ValueError("Failed to rename image")
        
        logging.info(f"Successfully processed and renamed {image_file} to {new_filename}")
        return None, new_filename  # Success: No failed file, return new filename
    except Exception as e:
        logging.error(f"Error processing {image_file}: {e}")
        return image_file, None  # Failure: Return failed file, no new filename

def process_images_parallel(image_files):
    """Process multiple images using multi-threading."""
    renamed_files, failed_files = [], []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Limit threads
        results = executor.map(process_single_image, image_files)

    for failed, renamed in results:
        if failed:
            failed_files.append(failed)
            src_path = os.path.join(IMAGE_FOLDER, failed)
            dst_path = os.path.join(FAILED_FOLDER, failed)
            
            # Check if the source file exists before moving
            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
            else:
                logging.error(f"File not found: {src_path}")
        if renamed:
            renamed_files.append(renamed)

    return renamed_files, failed_files

def process_and_zip(uploaded_files):
    """Processes images using OCR and returns ZIP file paths."""
    image_files = []
    for file in uploaded_files:
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            st.warning(f"Skipping {file.name} (too large).")
            continue
        
        file_path = os.path.join(IMAGE_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        image_files.append(file.name)

    renamed_files, failed_files = process_images_parallel(image_files)  # Use parallel processing

    success_zip = create_zip(OUTPUT_FOLDER, ZIP_SUCCESS.replace(".zip", "")) if renamed_files else None
    failed_zip = create_zip(FAILED_FOLDER, ZIP_FAILED.replace(".zip", "")) if failed_files else None

    cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER)
    return success_zip, failed_zip

# Streamlit UI
st.markdown(
    """
    <style>
    @keyframes scrollText {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .scrolling-text {
        white-space: nowrap;
        overflow: hidden;
        position: relative;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        color: #0066cc;
    }
    .scrolling-text span {
        display: inline-block;
        animation: scrollText 10s linear infinite;
    }
    .title {
        font-size: 30px;
        font-weight: bold;
        color: #ff5733;
        text-align: center;
        font-family: 'Georgia', serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .developer-credit {
        font-size: 14px;
        text-align: center;
        margin-top: 20px;
        color: #555;
    }
    </style>
    <div class='scrolling-text'><span>Blacklead Infratech PVT LTD</span></div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>OCR Model for BIPL</div>", unsafe_allow_html=True)

# File uploader with custom styling
uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Process button with custom styling
if st.button("Process Images", key="process_button"):
    if uploaded_files:
        # Clean up folders before processing
        cleanup_folders(OUTPUT_FOLDER, FAILED_FOLDER, DEBUG_FOLDER)
        
        with st.spinner("Processing images..."):
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            success_zip, failed_zip = process_and_zip(uploaded_files)
            progress_bar.progress(1.0)  # Complete progress bar

        st.success("Processing Completed!")

        # Store ZIP file paths in session state
        if success_zip:
            st.session_state.success_zip = success_zip
        if failed_zip:
            st.session_state.failed_zip = failed_zip

# Display download buttons if ZIP files exist in session state
if "success_zip" in st.session_state or "failed_zip" in st.session_state:
    col1, col2 = st.columns(2)

    if "success_zip" in st.session_state:
        with open(st.session_state.success_zip, "rb") as file:
            col1.download_button(
                label="Download Processed Images (ZIP)",
                data=file,
                file_name=ZIP_SUCCESS,
                mime="application/zip"
            )

    if "failed_zip" in st.session_state:
        with open(st.session_state.failed_zip, "rb") as file:
            col2.download_button(
                label="Download Failed Images (ZIP)",
                data=file,
                file_name=ZIP_FAILED,
                mime="application/zip"
            )
else:
    st.warning("Please upload images and click 'Process Images' to generate ZIP files.")

# Developer credit
st.markdown("<div class='developer-credit'>Developed by Rakesh Rathaur</div>", unsafe_allow_html=True)