import json
import os
import ocr_tag

DATA_FILE = "library.json"

def get_material_data(image_file):
    """
    image_file: can be a Streamlit UploadedFile (has .read()) or a camera input object.
    Your ocr_tag.ocr_text should handle it as currently written.
    """
    text = ocr_tag.ocr_text(image_file)
    fields = ocr_tag.extract_fields(text)

    return [
        f"Description: {fields.get('description', '')}",
        f"Price: {fields.get('price', 0)}",
    ]

def save_to_library(list_data):
    # Appends new items to the library.json file
    data = load_library()
    data.append(list_data)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_library():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def delete_item(index):
    data = load_library()
    if 0 <= index < len(data):
        data.pop(index)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

def calculate_total(price, qty):
    return round(float(price) * int(qty), 2)