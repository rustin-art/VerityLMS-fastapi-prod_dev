from pathlib import Path
import fitz  # PyMuPDF


def pdf_to_images(pdf_path: str, dpi: int = 200):
    """
    Converts PDF → list of image file paths using PyMuPDF
    """

    doc = fitz.open(pdf_path)
    output = []

    for idx, page in enumerate(doc):

        # render page to image
        pix = page.get_pixmap(dpi=dpi)

        image_path = (
            Path(pdf_path).parent /
            f"{Path(pdf_path).stem}_{idx}.png"
        )

        pix.save(str(image_path))

        output.append(str(image_path))

    return output