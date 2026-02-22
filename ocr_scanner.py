"""
Feature 2: Screenshot OCR Scanner
Extracts text from uploaded images using Tesseract OCR.
Supports English, Hindi, Tamil, Telugu.
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import re


def preprocess_image(image_bytes):
    """Enhance image for better OCR accuracy."""
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to RGB if needed
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')

    # Upscale small images
    w, h = img.size
    if w < 800:
        scale = 800 / w
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    # Enhance contrast and sharpness
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)

    return img


def extract_text_from_image(image_bytes):
    """
    Extract text from image bytes using Tesseract OCR.
    Returns (extracted_text, success, error_message)
    """
    # Check if Tesseract is installed
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        return "", False, "Tesseract OCR is not installed. Please install it with: brew install tesseract"

    try:
        img = preprocess_image(image_bytes)

        # Try English first (always available), then multi-language
        configs = [
            ('eng', '--psm 6'),                # English — block of text
            ('eng', '--psm 3'),                # English — auto detect
            ('eng', '--psm 4'),                # English — single column
        ]

        # Try adding multilingual support if available
        try:
            test = pytesseract.image_to_string(img, lang='eng+hin+tam+tel', config='--psm 6')
            if test.strip():
                configs.insert(0, ('eng+hin+tam+tel', '--psm 6'))
        except Exception:
            pass  # Multi-language packs not installed, skip

        best_text = ""
        for lang, config in configs:
            try:
                text = pytesseract.image_to_string(img, lang=lang, config=config)
                text = text.strip()
                if len(text) > len(best_text):
                    best_text = text
            except Exception:
                continue

        if not best_text:
            return "", False, "Could not extract text from image. Ensure the image is clear and contains readable text."

        # Clean up OCR artifacts — keep ASCII printable chars, newlines, and Indian scripts
        best_text = re.sub(r'[^\x20-\x7E\n\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F]', '', best_text)
        best_text = re.sub(r'\n{3,}', '\n\n', best_text).strip()

        if len(best_text) < 3:
            return "", False, "Could not extract meaningful text from image. Try a clearer screenshot."

        return best_text, True, None

    except Exception as e:
        return "", False, f"OCR processing error: {str(e)}"
