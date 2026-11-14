import os
import io
import fitz
from fontTools import subset

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PDF = os.path.join(BASE_DIR, "template_certificate.pdf")
ROBOTO_FONT = os.path.join(BASE_DIR, "static", "Roboto-Regular.ttf")

DEFAULT_NAME = "mtu skthu"
DEFAULT_DATE = "13 November 2026"
ORIGINAL_PDF_NAME = "dijen khuraijam"

def get_subset_font(text: str) -> bytes:
    options = subset.Options()
    options.drop_tables += ["gasp", "fpgm", "prep", "cvt "]
    font = subset.load_font(ROBOTO_FONT, options)
    sub = subset.Subsetter(options=options)
    sub.populate(text=text + " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,/-")
    sub.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, options)
    return buf.getvalue()

def generate_pdf(name: str = DEFAULT_NAME, date: str = DEFAULT_DATE) -> bytes:
    name = (name or DEFAULT_NAME).strip()
    date = (date or DEFAULT_DATE).strip()

    doc = fitz.open(TEMPLATE_PDF)
    page = doc[0]

    # Redact original name
    page.add_redact_annot(fitz.Rect(38.0, 275.0, 600.0, 325.0), fill=(1, 1, 1))

    # Redact date if changed
    if date and date != DEFAULT_DATE:
        page.add_redact_annot(fitz.Rect(605.0, 490.0, 780.0, 520.0), fill=(1, 1, 1))

    # Crucial: PDF_REDACT_IMAGE_NONE preserves background JPEG image, keeping file ~350 KB
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    # Embed lightweight subset font
    sub_bytes = get_subset_font(f"{name} {date}")
    page.insert_font(fontname="roboto", fontbuffer=sub_bytes)

    # Insert name at exact baseline (40, 308.28)
    page.insert_text(fitz.Point(40.0, 308.28), name, fontname="roboto", fontsize=20.0, color=(0, 0, 0))

    # Insert date at exact baseline (611.65, 510.28)
    if date and date != DEFAULT_DATE:
        page.insert_text(fitz.Point(611.65, 510.28), date, fontname="roboto", fontsize=14.0, color=(0, 0, 0))

    out_bytes = doc.tobytes(deflate=True, deflate_fonts=True, garbage=4, clean=True)
    doc.close()
    return out_bytes

def generate_certificate(name: str = DEFAULT_NAME, date: str = DEFAULT_DATE, output_pdf_path: str = None, output_image_path: str = None, dpi: int = 300, **kwargs):
    pdf_bytes = generate_pdf(name, date)
    if output_pdf_path:
        with open(output_pdf_path, "wb") as f:
            f.write(pdf_bytes)
    if output_image_path:
        doc = fitz.open("pdf", pdf_bytes)
        pix = doc[0].get_pixmap(dpi=dpi)
        pix.save(output_image_path)
        doc.close()
    return {"pdf_path": output_pdf_path, "image_path": output_image_path}
