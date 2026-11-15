from receipt_reader import read_receipt

with open("../eval/receipts/receipt_01.jpeg", mode="rb") as file:
    image_bytes = file.read()

receipt = read_receipt(image_bytes=image_bytes, mime_type="image/jpeg")

print(receipt.total)
print(receipt.tax)

item_sum = 0.00
for item in receipt.items:
    print(item.clean_name, item.category, item.price)
    item_sum += item.price

difference = round((receipt.total - item_sum - receipt.tax), 2)
print(difference)

if(difference != 0):
    print(f"Mismatch: this much is unaccounted for: {difference}")
else:
    print("Receipt adds up!")
