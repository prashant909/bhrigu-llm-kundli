import fitz  # PyMuPDF
import os

def extract_pdf(pdf_path, out_dir="bhrigu_output"):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    all_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        all_text += f"\n--- Page {page_num + 1} ---\n{text}"

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img_ext = base_image["ext"]
            with open(f"{out_dir}/page_{page_num+1}_img_{img_index}.{img_ext}", "wb") as f:
                f.write(image_bytes)

    with open(f"{out_dir}/bhrigu_text.txt", "w", encoding="utf-8") as f:
        f.write(all_text)

    print("✅ Extracted text & images to", out_dir)
