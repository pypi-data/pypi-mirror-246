from setuptools import setup, find_packages


# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NT_TextFileLoader",
    version="0.1.1",
    description=(
        "Python library to extract text from various file formats. "
        "The supported formats are: JPEG, PNG, PDF, DOCX, DOC, and TEXT."
    ),

    long_description=long_description,
    long_description_content_type="text/markdown",
    readme = "README.md",
    author="Vishnu.D",
    author_email="vishnu.d@narmtech.com",
    license="MIT",
    keywords =["pip install NT-TextLoader","pip install TextFileLoader","pip install NT Loader" ,"pip install textloader","pip install nt-textfileloader","pip install textfileloader"],
    packages=find_packages(),
    install_requires=[
            "PyPDF2==3.0.1",
            "python-docx==1.1.0",
            "docx2txt==0.8",
            "Pillow==9.4.0",
            "pytesseract==0.3.10",
            "langchain==0.0.350",
            "unstructured==0.11.2",
            "PyMuPDF==1.23.7"
        ],


    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ]
)