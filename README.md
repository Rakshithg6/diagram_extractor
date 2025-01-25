# Complex PDF Diagram Extractor

This project provides a tool to extract diagrams from PDF files, classify them using the Gemini API, and generate contextual information. The app is built using **Streamlit**, making it easy to use and deploy.

## Features

- **Diagram Detection**: Detects diagrams from each page of a PDF.
- **Classification**: Uses the Gemini API to classify diagrams and provide context.
- **Diagram Visualization**: Displays extracted diagrams along with their context.
- **PDF Page Mapping**: Indicates which page the diagram was extracted from.

## Requirements

- Python 3.8 or above
- Libraries: 
  - `streamlit`
  - `pytesseract`
  - `PyMuPDF` (fitz)
  - `Pillow`
  - `requests`
  - `opencv-python`
  - `numpy`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/complex-pdf-diagram-extractor.git
   cd complex-pdf-diagram-extractor
