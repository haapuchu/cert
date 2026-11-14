import os
import sys
import argparse
from certificate_engine import generate_certificate, DEFAULT_NAME, DEFAULT_DATE, ORIGINAL_COURSE

def main():
    parser = argparse.ArgumentParser(
        description="MathWorks Certificate Name & Details Editor (Pixel-Perfect with Exact Roboto Font)"
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=DEFAULT_NAME,
        help=f"New recipient name to put on the certificate (default: '{DEFAULT_NAME}')"
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        default=False,
        help="Export as PDF named certificate.pdf"
    )
    parser.add_argument(
        "--image",
        action="store_true",
        default=False,
        help="Export as high-res 300 DPI PNG named certificate.png"
    )
    parser.add_argument(
        "--jpg",
        action="store_true",
        default=False,
        help="Export as JPEG image named certificate.jpg"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save the exported files (default: current directory)"
    )
    parser.add_argument(
        "--date",
        default=None,
        help=f"Optional date string (default: '{ORIGINAL_DATE}')"
    )
    parser.add_argument(
        "--course",
        default=None,
        help=f"Optional course title (default: '{ORIGINAL_COURSE}')"
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=20.0,
        help="Font size for recipient name in points (default: 20.0)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for exported image in DPI (default: 300)"
    )

    args = parser.parse_args()

    # If neither --pdf nor --image nor --jpg was explicitly given, generate both PDF and PNG!
    gen_pdf = args.pdf or (not args.image and not args.jpg)
    gen_png = args.image or (not args.pdf and not args.jpg)
    gen_jpg = args.jpg

    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    pdf_path = os.path.join(out_dir, "certificate.pdf") if gen_pdf else None
    png_path = os.path.join(out_dir, "certificate.png") if gen_png else None
    jpg_path = os.path.join(out_dir, "certificate.jpg") if gen_jpg else None

    print(f"Modifying certificate for: '{args.name}'")
    if args.date:
        print(f"Date: {args.date}")
    if args.course:
        print(f"Course: {args.course}")

    if gen_pdf or gen_png:
        res = generate_certificate(
            name=args.name,
            date=args.date,
            course_name=args.course,
            font_size=args.font_size,
            output_pdf_path=pdf_path,
            output_image_path=png_path,
            image_format="PNG",
            dpi=args.dpi
        )
        if pdf_path:
            print(f"[✓] Saved PDF: {pdf_path}")
        if png_path:
            print(f"[✓] Saved Image (PNG, {args.dpi} DPI): {png_path}")

    if gen_jpg:
        res_jpg = generate_certificate(
            name=args.name,
            date=args.date,
            course_name=args.course,
            font_size=args.font_size,
            output_image_path=jpg_path,
            image_format="JPEG",
            dpi=args.dpi
        )
        print(f"[✓] Saved Image (JPEG, {args.dpi} DPI): {jpg_path}")

    print("\nSuccess! All requested certificate files were generated.")

if __name__ == "__main__":
    main()
