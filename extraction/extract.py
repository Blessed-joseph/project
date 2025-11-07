import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image
import pytesseract
import re
import json
from pdf2image import convert_from_path

pdf_path = (
    "/home/blessed/Documents/projet_church/project/uploads/DAILY MANNA_2026.pdf"
)

pages = convert_from_path(pdf_path, dpi=300)

output_dir = Path(__file__).parent / "image"
output_dir.mkdir(parents=True, exist_ok=True)

# Enregistre chaque page sous forme d’image dans le dossier "image"
for i, page in enumerate(pages, start=1):
    image_path = output_dir / f"page_{i}.png"
    page.save(str(image_path), "PNG")


# on utilise pytesseract pour extraire le texte de chaque image
# je teste sur la première page
first_page_image = output_dir / "page_1.png"
image = Image.open(first_page_image)
texte = pytesseract.image_to_string(image)
print(texte)