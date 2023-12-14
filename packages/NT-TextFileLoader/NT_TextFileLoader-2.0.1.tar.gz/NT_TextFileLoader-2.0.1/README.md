# NT-TextLoader

[![N|Solid](https://narmtech.com/img/companylogo.png)](https://nodesource.com/products/nsolid)


### Description

  *A Python module for extracting text content from various file types including PDFs, DOCX, DOC, text files, and images using Optical Character Recognition (OCR).*


### Installation Instructions

Before using this package, ensure you have installed the following system-level dependencies:

### 1.On Linux
- Tesseract OCR and MS Office:

  ```bash
  !apt install tesseract-ocr
  !apt install libtesseract-dev
  !apt-get --no-install-recommends install libreoffice -y
  !apt-get install -y libreoffice-java-common

### 2.On Windows

Simple steps for tesseract installation in windows.

  - 1.Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.

  - 2.Install this exe in C:\Program Files (x86)\Tesseract-OCR

  - 3.Open virtual machine command prompt in windows or anaconda prompt.

  - 4.Run pip install pytesseract

To test if tesseract is installed type in python prompt:
```python 
import pytesseract
print(pytesseract)
 ```

## Installation

Install the package using pip:

```bash
pip install NT-TextFileLoader

```

## Usage

```python
from NT_TextFileLoader.text_loader import TextFileLoader

# Load text from a file
file_path = 'path/to/your/file'
extracted_text = TextFileLoader.load_text(file_path,min_text_length=50) 
# If the ouput length is lesser than 50(min_text_length) then OCR will be used to extract text.
# Increate the min_text_length value to use OCR.
print(extracted_text)
```

## Supported File Types

- **PDF**: Extracts text from PDF files.
- **DOCX**: Extracts text from DOCX files.
- **DOC**: Extracts text from legacy DOC files.
- **Text files**: Loads text content from TXT files.
- **Images (JPG, PNG, JPEG, WEBP)**: Uses OCR to extract text from images.

## Requirements

- PyPDF2
- python-docx
- Pillow
- pytesseract (For image-based text extraction)
- langchain 
- unstructured
- docx2txt
- PyMuPDF

## Contributions

Contributions, issues, and feature requests are welcome!

## License

This project is licensed under the MIT License.
