import streamlit as st
import pytesseract
from PIL import Image
import json
import pickle

# Set the path for the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Streamlit app title
st.title("OCR-based Document Verification")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an ID image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)

    # Split the text by new lines and filter out empty lines
    lines = [line for line in text.split('\n') if line.strip()]

    # Initialize an empty dictionary to hold the key-value pairs
    data = {}

    # Process each line to extract the key-value pairs
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()  # Convert to lowercase for flexible matching
            value = value.strip()
            data[key] = value
        else:
            parts = line.split(' ', 1)
            if len(parts) == 2:
                key, value = parts
                key = key.strip().lower()  # Convert to lowercase for flexible matching
                value = value.strip()
                data[key] = value

    # Convert the dictionary into JSON format
    json_data = json.dumps(data, indent=4)

    # Save the JSON data into a pickle file
    with open('json_data.pkl', 'wb') as f:
        pickle.dump(json_data, f)

    # Display the extracted JSON data
    st.subheader("Extracted Data in JSON Format:")
    st.json(json_data)

    # Predefined keys for input and comparison
    keys = [
        "Name", 
        "Parent", 
        "Course/Branch", 
        "enrollment no.", 
        "blaod group", 
        "em\u00e9tgency no.", 
        "valid"
    ]

    # Function to normalize values for comparison
    def normalize(value):
        try:
            # Try to convert to integer
            return int(value)
        except ValueError:
            try:
                # Try to convert to float
                return float(value)
            except ValueError:
                # Convert to lowercase string for case-insensitive comparison
                return str(value).strip().lower()

    # Take input from the user for each key and verify against the extracted data
    verification_results = {}
    for key in keys:
        normalized_key = key.strip().lower()  # Normalize key for flexible matching
        user_value = st.text_input(f"Enter the value for {key}: ").strip()
        
        if user_value:
            # Normalize user input
            user_value = normalize(user_value)
            
            # Normalize and compare extracted data
            if normalized_key in data:
                extracted_value = normalize(data[normalized_key])
                
                # Check if the key exists in the extracted data and if the value matches
                if extracted_value == user_value:
                    st.write(f"{key}: VERIFIED")
                    verification_results[key] = "VERIFIED"
                else:
                    st.write(f"{key}: NOT VERIFIED")
                    verification_results[key] = "NOT VERIFIED"
            else:
                st.write(f"{key}: KEY NOT FOUND")
                verification_results[key] = "KEY NOT FOUND"

    # Save the verification results into a pickle file
    with open('verification.pkl', 'wb') as f:
        pickle.dump(verification_results, f)

    # Option to download the verification results
    st.download_button(
        label="Download Verification Results",
        data=pickle.dumps(verification_results),
        file_name="verification.pkl",
        mime="application/octet-stream"
    )
