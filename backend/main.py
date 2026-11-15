from fastapi import FastAPI, UploadFile
from receipt_reader import read_receipt

# creating the app obj so that every route have one place to attach
app =  FastAPI()

# adding a health check route to confirm that the server is running
# before adding any features
@app.get("/health")
def health():
    return { "status": "ok" }

# Accepting a photo upload so the frontend
# can send receipts to be read
@app.post("/receipts")
def upload_receipt(file: UploadFile):
    image_bytes = file.file.read()
    receipt = read_receipt(image_bytes=image_bytes, mime_type=file.content_type)
    return receipt