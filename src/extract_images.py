"""
Script para extraer imágenes del PDF del examen MIR 2026.
Las primeras 25 preguntas tienen imágenes asociadas.

El PDF final del MIR contiene muchas imágenes pequeñas (fragmentos de texto/fuentes PNG)
y las imágenes reales del examen son JPEG de mayor tamaño (>30KB).
Este script filtra para quedarse solo con las imágenes relevantes.
"""
import fitz  # pymupdf
import os
import glob

# Configuración
pdf_path = "data/26/MIR26_final.pdf"  # PDF final oficial
out_dir = "images/26"

# Página inicial (las imágenes del examen empiezan en la página 3)
# Las páginas 1-2 contienen texto/instrucciones con fragmentos de fuentes como imágenes
START_PAGE = 3

# Tamaño mínimo en bytes para considerar una imagen como relevante (30KB)
# Las imágenes médicas reales del examen son JPEG de 40KB-180KB
# Los fragmentos de texto son PNG de ~10-12KB
MIN_IMAGE_SIZE = 30000

# Formatos permitidos (las imágenes del examen son JPEG)
# Dejar vacío para aceptar todos los formatos que pasen el filtro de tamaño
ALLOWED_FORMATS = []  # Aceptar todos los formatos desde la página 3

# Limpiar imágenes anteriores si existen
if os.path.exists(out_dir):
    old_images = glob.glob(os.path.join(out_dir, "image_*"))
    if old_images:
        print(f"Eliminando {len(old_images)} imágenes anteriores...")
        for img in old_images:
            os.remove(img)
        print("Imágenes anteriores eliminadas.\n")

os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# Primera pasada: recopilar todas las imágenes relevantes
relevant_images = []

for page_index in range(START_PAGE - 1, len(doc)):  # Empezar desde START_PAGE (índice 0-based)
    page = doc[page_index]
    images = page.get_images(full=True)

    for img_index, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        image_bytes = base["image"]
        ext = base["ext"]
        
        # Filtrar por formato si se especifica
        if ALLOWED_FORMATS and ext.lower() not in ALLOWED_FORMATS:
            continue
            
        # Filtrar por tamaño mínimo
        if len(image_bytes) >= MIN_IMAGE_SIZE:
            relevant_images.append({
                "bytes": image_bytes,
                "ext": ext,
                "page": page_index + 1,
                "size": len(image_bytes)
            })

# Segunda pasada: guardar las imágenes con numeración correcta (1-25)
print(f"Encontradas {len(relevant_images)} imágenes relevantes")
print(f"  - Páginas: {START_PAGE} a {len(doc)}")
print(f"  - Formato: {ALLOWED_FORMATS if ALLOWED_FORMATS else 'todos'}")
print(f"  - Tamaño mínimo: {MIN_IMAGE_SIZE / 1024:.0f} KB\n")

for idx, img_data in enumerate(relevant_images, start=1):
    img_name = f"image_{idx}.{img_data['ext']}"
    with open(os.path.join(out_dir, img_name), "wb") as f:
        f.write(img_data["bytes"])
    size_kb = img_data["size"] / 1024
    print(f"Extraída: {img_name} (página {img_data['page']}, {size_kb:.1f} KB)")

print(f"\nTotal: {len(relevant_images)} imágenes extraídas en {out_dir}")
