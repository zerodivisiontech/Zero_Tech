Material Handler (Prototype)

Status: Prototype / Lab App
Repository: ZeroDivisionTech

Overview

Material Handler is a prototype application that captures information from retail tags (via image OCR) and converts it into structured data that can be saved and organized in a simple vault/library system.

The application was built to test a workflow where a user can photograph a product tag, automatically extract useful fields (description, price, item number), and store those results for later reference.

The project successfully demonstrates the following pipeline:

Image Upload → OCR Extraction → Field Parsing → Editable Draft → Save to Library

While functional, the current implementation is still experimental and the field structure will likely change in future versions.

---

Current Features

- Image upload or tag photo input
- OCR processing using Tesseract
- Automatic extraction of:
  - Description
  - Price
  - Item number (when detected)
- Editable draft fields in the workbench
- Save results to a local vault/library
- Simple interface built with Streamlit

---

Known Limitations

- OCR accuracy depends on lighting and image clarity
- Parsing logic is currently tuned toward retail price tags (ex: Lowe’s clearance tags)
- Description detection sometimes selects the longest text line rather than the correct product name
- Item number extraction requires clear labeling in the tag

---

Planned Improvements

Future versions should restructure the data fields and parsing rules.

Proposed field model:

- Description – extracted automatically from OCR text
- Item Number – detected from labeled tag fields (e.g., “Item #”)
- Price – extracted from OCR with preference for current price over historical (“Was”) price
- Notes – user-entered context or comments
- Raw OCR Text – stored internally for debugging or improved parsing later

Separating machine-extracted fields from user-entered notes will improve reliability and prevent OCR output from overwriting user context.

---

How to Run

Create a virtual environment and install dependencies:

pip install -r requirements.txt

Run the interface:

streamlit run interface.py

---

Purpose of This Project

This project serves as a proof-of-concept for image-to-data workflows and helped explore:

- OCR pipelines
- text parsing strategies
- Streamlit interface development
- rapid prototyping of utility applications

Even if the final concept evolves, the knowledge gained from building this system is intended to inform future projects inside the ZeroDivisionTech ecosystem. This apps logic was run through 
Packager.py file you can find in the tools folder of the repo as a test to see how it worked 