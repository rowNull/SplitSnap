from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

class Item(BaseModel):
    name: str
    price: float
    clean_name: str
    category: Literal["shared", "personal"]


class Receipt(BaseModel):
    store: str
    total: float
    tax: float
    card_last4: str
    items: list[Item]

# loading the key from .env so it never has be written in code
load_dotenv()
client = genai.Client()

with open("../eval/receipts/receipt_01.jpeg", mode="rb") as file:
    image_bytes = file.read()
image_part = types.Part.from_bytes(
    data=image_bytes, 
    mime_type="image/jpeg"
    )

with open("./house_rules.txt", mode="r") as file:
    rules = file.read()

prompt = f"Extract the store name, total, tax, last 4 card digits and every line item with its price from this receipt. Do not include tax as a line item. For each item, also give a clean readable name and a category of shared or personal, following these house rules: {rules}"

# using the flash model since it is the fastest and cheapest for testing
response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=[image_part, prompt], config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Receipt))

print(response.text)
print(response.parsed.total)
print(response.parsed.tax)

item_sum = 0.00
for item in response.parsed.items:
    print(item.clean_name, item.category, item.price)
    item_sum += item.price

difference = round((response.parsed.total - item_sum - response.parsed.tax), 2)
print(difference)

if(difference != 0):
    print(f"Mismatch: this much is unaccounted for: {difference}")
else:
    print("Receipt adds up!")
