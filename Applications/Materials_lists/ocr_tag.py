import re
from PIL import Image, ImageOps as imageops
import pytesseract

PRICE_RE = re.compile(r"\$?\s*(\d{1,4})(?:\.(\d{1,2}))?")

def ocr_text(image_file):
    img = Image.open(image_file)
    img = imageops.exif_transpose(img)
    gray = img.convert('L')
    gray = imageops.autocontrast(gray)
    bw = gray.point(lambda x: 0 if x < 160 else 255, '1')
    config = "--psm 6 --oem 3"
    text = pytesseract.image_to_string(bw, config=config)
    
    #print(f"DEBUG OCR LENGTH: {len(text)}")
    #print(f"DEBUG OCR text: {repr(text[:200])}")
    #print(f"DEBUG OCR text (full): {repr(text)}")
    #print("DEBUG IMAGE SIZE:", img.size)
    #print("debug raw ocr", repr(text))

    return text

def extract_fields(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    full = " ".join(lines)

    price = None
    match = PRICE_RE.search(full)
    if match:
        dollars, cents = match.groups()
        if not cents:
            cents = "00"
        elif len(cents) == 1:
            cents += "0"
        price = float(f"{dollars}.{cents}")

    description = lines[0] if lines else ""

    return {
        "description": description,
        "price": price or 0.0
    }