import cv2
import pytesseract
from PIL import Image
import json
import pickle
import streamlit as st

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Streamlit UI
st.title("SUBMIT THE APPLICATION")

# Upload an image file
uploaded_file = st.file_uploader("UPLOAD THE APPLICATION", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption="Uploaded ID Image", use_column_width=True)

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.subheader("Extracted Text")
    st.text(text)

    # Split the text by new lines and filter out empty lines
    lines = [line for line in text.split('\n') if line.strip()]
    
    # Initialize an empty dictionary to hold the key-value pairs
    data = {}
    
    # Process each line to extract the key-value pairs
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
        else:
            key, value = line.split(' ', 1)
        key = key.strip()
        value = value.strip()
        data[key] = value

    # Convert the dictionary into JSON format
    json_data = json.dumps(data, indent=4)

    # Dump the JSON data into a pickle file
    with open('json_data.pkl', 'wb') as f:
        pickle.dump(json_data, f)

    # Display the JSON data
   # st.subheader("Extracted Data in JSON Format")
   # st.json(json_data)

    # Predefined keys for input and comparison
    keys = [
        "Name", 
        "Parent", 
        "Course/Branch", 
        "Enroliment No.", 
        "Blaod Group", 
        "Emergency No.", 
        "Valid"
    ]

    # Input verification
    st.subheader("Verify the Extracted Data")

    for key in keys:
        user_value = st.text_input(f"Enter the value for {key}: ")
        
        # Convert both values to strings for comparison
        extracted_value = str(data.get(key, ""))
        user_value = str(user_value).strip()

        # Check if the key exists in the extracted data and if the value matches
        if extracted_value == user_value:
            st.success(f"{key}: VERIFIED")
        else:
            st.error(f"{key}: NOT VERIFIED")
            
    # Save verification results (you can customize the model_data variable as per your requirements)
    model_data = data  # Assuming model_data is derived from the data dictionary

    with open('verification.pkl', 'wb') as f:
        pickle.dump(model_data, f)

    st.success("Verification results saved.")
