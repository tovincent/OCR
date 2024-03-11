#pip install pymupdf pytesseract pillow

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def search_in_pdf(pdf_path, search_string):
    pdf_document = fitz.open(pdf_path)
    found_pages = []
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        text = ""
        
        for image_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text += pytesseract.image_to_string(image)
        
        # Search for the string in the extracted text
        if search_string.lower() in text.lower():
            found_pages.append(page_num)
    
    return found_pages

# Path to your PDF file
pdf_path = 'path_to_your_pdf_file.pdf'
search_string = "Hello world"

# Search for the string in the PDF
pages_with_search_string = search_in_pdf(pdf_path, search_string)

if pages_with_search_string:
    print(f'The string "{search_string}" was found on page(s): {", ".join(map(str, pages_with_search_string))}')
else:
    print(f'The string "{search_string}" was not found in the document.')
