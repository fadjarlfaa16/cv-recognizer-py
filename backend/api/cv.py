import tempfile
import os
from fastapi import APIRouter, File, UploadFile
import pytesseract
from pdf2image import convert_from_path
from openai import OpenAI


with open("scope2.txt", "r", encoding="utf-8") as file:
    isi = file.read()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",  # Change with your API
)

router = APIRouter()

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    print("Receiving request upload, content type:", file.content_type)
    if file.content_type != "application/pdf":
        return {"error": "File type must be PDF!."}
    
    file_bytes = await file.read()
    print("File size:", len(file_bytes))
    
    try:
        # Making Temporary File
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.write(file_bytes)
        tmp.close()
        print("Temporary file saved in:", tmp.name)
        
        # Ensure the poppler installed bt checking the path
        poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
        images = convert_from_path(tmp.name, poppler_path=poppler_path)
        os.unlink(tmp.name)  # Delete Temporary File
    except Exception as e:
        print("Error while conversing to PDF:", e)
        return {"error": "Failed convert to image.", "detail": str(e)}
    
    extracted_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, config="--psm 6")
        extracted_text += text + "\n"
    
    print("CV Scan Succesfully!")
    
    # Call Open Router API 
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  
                "X-Title": "<YOUR_SITE_NAME>",      
            },
            extra_body={},
            # add your model name here
            model="<model>",
            messages=[
                {
                    "role": "user",
                    "content": extracted_text + "\n \n " + isi  # OCR Result + Scope
                }
            ]
        )
        openrouter_response = completion.choices[0].message.content
    except Exception as e:
        print("Error saat memanggil OpenRouter API:", e)
        openrouter_response = f"Error calling OpenRouter API: {str(e)}"
    
    return {
        "message": "Berhasil",
        "extracted_text": extracted_text,
        "openrouter_response": openrouter_response
    }
