from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
import re
import cv2
import numpy as np




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_value(text, pattern):
    """Return first match of a regex pattern from OCR text."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None

@app.post("/verify")
async def verify_label(
    brand_name: str = Form(...),
    product_type: str = Form(...),
    alcohol_content: str = Form(...),
    net_contents: str = Form(""),
    image: UploadFile = None
):

    if not image:
        return {"success": False, "details": {"error": "No image uploaded"}}

    # Read image
    img_bytes = await image.read()
    img = Image.open(io.BytesIO(img_bytes))

    big = cv2.resize(np.array(img), None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    # OCR
    extracted_text = pytesseract.image_to_string(big)
    extracted_text = extracted_text.lower()
    # print(extracted_text)
    brand_name = brand_name.lower()
    product_type = product_type.lower()
    alcohol_content = alcohol_content.lower()
    net_contents = net_contents.lower()

    extracted = {
        "brand_name": extract_value(extracted_text, rf"\b{brand_name}\b"),
        "product_type": extract_value(extracted_text, rf"\b{product_type}\b"),
        "alcohol_content": extract_value(extracted_text, r"\b\d+(\.\d+)?\s*%"),
        "net_contents": extract_value(extracted_text, r"\b\d+\s*(ml|mL|oz|OZ)\b"),
        "gov_warning": extract_value(extracted_text, r"\bGOVERNMENT WARNING\b")
    }
    
    num_label_AC = int(re.search(r'\d+', extracted["alcohol_content"]).group())
    num_label_NC = int(re.search(r'\d+', extracted["net_contents"]).group())
    num_input_AC = int(re.search(r'\d+', alcohol_content).group())
    num_input_NC = int(re.search(r'\d+', net_contents).group())

    response = {
        "brand_name": {
            "form_value": brand_name,
            "ocr_value": extracted["brand_name"],
            "match": extracted["brand_name"] is not None
        },
        "product_type": {
            "form_value": product_type,
            "ocr_value": extracted["product_type"],
            "match": extracted["product_type"] is not None
        },
        "alcohol_content": {
            "form_value": alcohol_content,
            "ocr_value": extracted["alcohol_content"],
            "match": num_label_AC == num_input_AC and alcohol_content in extracted_text
        },
        "net_contents": {
            "form_value": net_contents,
            "ocr_value": extracted["net_contents"],
            "match": num_label_NC == num_input_NC and net_contents in extracted_text
        },
        "gov_warning": {
            "match": extracted["gov_warning"] is not None
        } #,
        #"full_ocr_text": extracted_text
    }

    # Determine full success
    success = all(section["match"] for section in response.values() if isinstance(section, dict))

    return {
        "success": success,
        "results": response
    }
