"""
Module for loading text from different file types.
"""

import PyPDF2
import docx
from PIL import Image
import pytesseract
import tempfile
from langchain.document_loaders import UnstructuredWordDocumentLoader
import os
import tempfile
import fitz  # PyMuPDF
from PIL import Image
import shutil
from tqdm import tqdm  # Import tqdm for the progress bar

class TextFileLoader:
    """
    Class for loading text from various file types.
    """

    @staticmethod
    def load_text(file_path,min_text_length=50):

        """
        Load text from different file types.

        Args:
        - file_path (str): Path to the file to be loaded.
        - min_text_length (int) : Minimum required length of output text.(set it above 50 to use OCR)

        Returns:
        - str: Extracted text from the file.
        """

        try:
          file_type = file_path.split(".")[-1]

          if file_type == 'pdf':
              out =  TextFileLoader.load_pdf(file_path)
              if len(out)<100:
                print("-----------------------Please Note ---------------------------")
                print("If you think the extracted information is wrong then increase the 'min_text_length' parameter above 50 to use OCR!!!.")
              return out

          elif file_type == 'docx':
              return TextFileLoader.load_docx(file_path)
          elif file_type == 'doc':
              return TextFileLoader.load_doc(file_path)
          elif file_type == 'txt':
              return TextFileLoader.load_text_file(file_path)
          elif file_type.lower() in (("jpg,png,jpeg,webp")):
              return TextFileLoader.load_image(file_path)
          else:
              return "File type not supported"
        except Exception as e:
            return f"Error loading file: {str(e)}"

    @staticmethod
    def load_pdf(file_path,min_text_length=50):

        """
        Load text from a PDF file.

        Args:
        - file_path (str): Path to the PDF file.
        - min_text_length (int) : Minimum required length of outpu text.(set it above 50 to use OCR)

        Returns:
        - str: Extracted text from the PDF.
        """
        try:
          with open(file_path, 'rb') as file:
              pdf_reader = PyPDF2.PdfReader(file)
              text = ''
              for page_num in range(len(pdf_reader.pages)):
                  page = pdf_reader.pages[page_num]
                  text += page.extract_text()
              # Check if extracted text has enough length
              if len(text) >= min_text_length:
                  return text
              else:
                temp_dir = TextFileLoader.pdf_to_images(file_path)
                images = [os.path.join(temp_dir,i) for i in os.listdir(temp_dir) if i.endswith(".png")]
                # Use OCR to extract text from images
                with tqdm(total=len(images),desc="Extracting text using OCR: Sit back and relax, this may take some time") as pbar:
                  extracted_text = ''
                  page_number = 0
                  for img_path in images:
                    try:
                      pbar.update(1)
                      pbar.set_description(f"Extracting text from image {page_number + 1}/{len(images)}")
                      image = Image.open(img_path)
                      ocr_text = pytesseract.image_to_string(image)
                      extracted_text += ocr_text + '\n'
                      page_number+=1
                    except:
                      pbar.set_description(f"Ignoring Page {page_number + 1}/{len(images)}")
                      pass

                shutil.rmtree(temp_dir)
                return extracted_text.strip() if extracted_text else "No text found in the PDF"
        except Exception as e:
            return f"Error loading PDF or extracting text: {str(e)}"

    @staticmethod
    def load_docx(file_path):

        """
        Load text from a DOCX file.

        Args:
        - file_path (str): Path to the DOCX file.

        Returns:
        - str: Extracted text from the DOCX.
        """

        try:
            doc = docx.Document(file_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text
            return text
        except Exception as e:
            return f"Error loading DOCX: {str(e)}"

    @staticmethod
    def load_doc(file_path):
      
        """
        Load text from a DOC file.

        Args:
        - file_path (str): Path to the DOC file.

        Returns:
        - str: Extracted text from the DOC.
        """

        try:
            loader = UnstructuredWordDocumentLoader(file_path)
            data = loader.load()
            text = ""
            for i in range(len(data)):
                text=text+"\n"+data[i].page_content
            return text.strip()
        except Exception as e:
            return f"Error loading DOC: {str(e)}"

    @staticmethod
    def load_text_file(file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
            return text
        except Exception as e:
            return f"Error loading text file: {str(e)}"

    @staticmethod
    def load_image(file_path):

        """
        Load text from a text file.

        Args:
        - file_path (str): Path to the text file.

        Returns:
        - str: Extracted text from the text file.
        """

        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip() if text else "No text found in the image"
        except Exception as e:
            return f"Error loading image or extracting text: {str(e)}"

    @staticmethod
    def pdf_to_images(pdf_path):

      """
      Convert a PDF file into images and store them in a temporary folder.

      Args:
      - pdf_path (str): The path to the PDF file to be converted.

      Returns:
      - str: The path to the temporary folder containing the converted images.
              If an error occurs during conversion, returns an error message.
      """
      try:
        # Create a temporary folder to store images
        temp_folder = tempfile.mkdtemp(dir=".")

        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        image_no ="1"
        # Iterate through each page and convert it to an image
        with tqdm(total=pdf_document.page_count) as pbar:
          image_no = "1"
          # Iterate through each page and convert it to an image
          for page_number in range(pdf_document.page_count):
              # Update the progress bar
              pbar.update(1)
              # Set custom description for the progress bar
              pbar.set_description(f"Extracting text using OCR - Converting pdf {page_number + 1}/{pdf_document.page_count} to image.")

              # Get the page
              page = pdf_document.load_page(page_number)

              # Get the pixel dimensions (DPI) of the page
              dpi = 300  # You can adjust the DPI as needed

              # Convert the PDF page to a Pillow Image
              image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
              pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

              # Save the image to the temporary folder
              image_path = os.path.join(temp_folder, image_no + ".png")
              pil_image.save(image_path, format="PNG")
              image_no = image_no + "1"

        # Close the PDF document
        pdf_document.close()
        return temp_folder
      except Exception as e:
        return f"Error While converting pdf into images: {str(e)}"