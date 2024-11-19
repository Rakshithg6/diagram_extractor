import streamlit as st
import fitz  # PyMuPDF for PDF parsing
from PIL import Image
from io import BytesIO
import pytesseract
import requests
import cv2
import numpy as np

# Preprocess image for diagram detection
def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary

# Detect diagrams in the image
def detect_diagrams(image):
    processed = preprocess_image(image)
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diagrams = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 50:  # Filter small areas
            diagram = image.crop((x, y, x + w, y + h))
            diagrams.append((x, y, w, h, diagram))
    return diagrams

# Classify diagrams using Gemini API
def classify_diagram(diagram, gemini_api_key):
    buffered = BytesIO()
    diagram.save(buffered, format="PNG")
    buffered.seek(0)
    files = {"file": ("diagram.png", buffered, "image/png")}
    headers = {"Authorization": f"Bearer {gemini_api_key}"}
    try:
        response = requests.post("https://gemini.api/diagrams", files=files, headers=headers)
        response.raise_for_status()
        return response.json().get("diagram_context", "No context provided")
    except Exception as e:
        return f"Error: {e}"

# Extract diagrams from the PDF
def extract_diagrams_from_pdf(uploaded_file, gemini_api_key):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    results = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Detect diagrams in the page image
        diagrams = detect_diagrams(image)
        for idx, (x, y, w, h, diagram) in enumerate(diagrams):
            context = classify_diagram(diagram, gemini_api_key)
            results.append({
                "page": page_num + 1,
                "diagram_number": idx + 1,
                "coordinates": (x, y, w, h),
                "context": context,
                "diagram_image": diagram
            })
    return results

# Streamlit App
st.title("Complex PDF Diagram Extractor")
st.write("Upload a PDF file to extract diagrams, classify them, and generate context.")

# File upload and API key input
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
gemini_api_key = st.text_input("Enter Gemini API Key", type="password")

if uploaded_file and gemini_api_key:
    st.write("Processing the PDF...")
    results = extract_diagrams_from_pdf(uploaded_file, gemini_api_key)
    
    if results:
        st.write(f"Extracted {len(results)} diagrams.")
        for result in results:
            st.write(f"Page: {result['page']}, Diagram {result['diagram_number']}")
            st.write(f"Context: {result['context']}")
            st.image(result['diagram_image'])
    else:
        st.write("No diagrams were found in the PDF.")
