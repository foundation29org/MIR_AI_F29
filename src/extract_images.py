"""
Script para extraer imágenes del PDF del examen MIR 2026.
Las primeras 25 preguntas tienen imágenes asociadas.
"""
import fitz  # pymupdf
import os

pdf_path = "data/MIR26.pdf"
out_dir = "images/26"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

img_count = 0
for page_index in range(len(doc)):
    page = doc[page_index]
    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        image_bytes = base["image"]
        ext = base["ext"]

        img_count += 1
        # Nombrar como image_1.png, image_2.png, etc. para mantener consistencia con años anteriores
        img_name = f"image_{img_count}.{ext}"
        with open(os.path.join(out_dir, img_name), "wb") as f:
            f.write(image_bytes)
        print(f"Extraída: {img_name} (página {page_index + 1})")

print(f"\nTotal: {img_count} imágenes extraídas en {out_dir}")
