from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

# Making a separate shape for each item 
# since one receipt holds many of them
class Item(BaseModel):
    name: str
    price: float
    clean_name: str

    # Limiting category to two choices so
    # Gemini can't invent its own labels
    category: Literal["shared", "personal"]


class Receipt(BaseModel):
    store: str
    total: float

    # Keeping tax separate from items since
    # it gets split differently than groceries
    tax: float

    # Storing last 4 as text since a number
    # would drop leading zeros like 0123
    card_last4: str
    items: list[Item]

# loading the key from .env so it never has be written in code
load_dotenv()
client = genai.Client()

# Reading rules once at startup so every
# receipt uses them without reopening the file
with open("./house_rules.txt", mode="r") as file:
    rules = file.read()

# Wrapping the Gemini call in a function
# so the API route and tests can share it
def read_receipt(image_bytes, mime_type):
    image_part = types.Part.from_bytes(
        data=image_bytes, 
        mime_type=mime_type
    )

    prompt = f"Extract the store name, total, tax, last 4 card digits and every line item with its price from this receipt. Do not include tax as a line item. List every printed line as its own item, including fees like CRV. Never combine lines. For each item, also give a clean readable name and a category of shared or personal, following these house rules: {rules}"


    # using the flash model since it is the fastest and cheapest for testing
    response = client.models.generate_content(model="gemini-3.5-flash-lite", contents=[image_part, prompt], config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Receipt, temperature=0))

    receipt = response.parsed
    receipt.store = receipt.store.capitalize()
    return receipt

