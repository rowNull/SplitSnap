from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

class Receipt(BaseModel):
    store: str
    total: float
    card_last4: str

# loading the key from .env so it never has be written in code
load_dotenv()
client = genai.Client()

with open("../eval/receipts/receipt_01.jpeg", mode="rb") as file:
    image_bytes = file.read()
image_part = types.Part.from_bytes(
    data=image_bytes, 
    mime_type="image/jpeg"
    )

# using the flash model since it is the fastest and cheapest for testing
response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=[image_part, "Extract the store name, total and last 4 card digits from this receipt."], config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Receipt))

print(response.text)
print(response.parsed.total)
