from pywinauto import Application
from withdraw import withdraw
from getItemCircStatus import getItemCircStatus
from itemData import extractItemData
import pandas as pd
import time
import os

app = Application(backend="win32").connect(title_re=".*Polaris ILS.*")
BARCODE_FILE = "barcodes7.txt"
DONE_FILE = "done.txt"
PARTIAL_FILE = "partial.csv"

polaris = app.window(title_re=".*Polaris ILS.*")
polaris.wait('ready')
polaris.type_keys("^%{F9}")

item_search = app.window(title="Item Records - Barcode Find Tool")
item_search.wait('exists', timeout=10)

with open(BARCODE_FILE, 'r') as f:
    barcodes = [line.strip() for line in f]

done = set()
if os.path.exists(DONE_FILE):
    with open(DONE_FILE) as f:
        done = {line.strip() for line in f}
    print(f"Resuming — skipping {len(done)} already processed")

barcodes = [b for b in barcodes if b not in done]

# barcodes = ["000961264"]

last_copies = []
if os.path.exists(PARTIAL_FILE):
    last_copies = pd.read_csv(PARTIAL_FILE, dtype={'Barcode': str}).to_dict('records')
    print(f"Loaded {len(last_copies)} partial results from previous run")

print(barcodes)
edits = item_search.children(class_name="Edit")
barcode_field = edits[2]

for barcode in barcodes:
    barcode_field.click_input()
    time.sleep(.3)
    item_search.type_keys(barcode)
    time.sleep(.3)
    item_search.type_keys("{ENTER}")
    time.sleep(.3)
    item_search.type_keys("{ENTER}")

    item_record = app.window(title_re=r"^Item Record \d+")
    item_record.wait('exists', timeout=10)

    withdraw(item_record)

    if not getItemCircStatus(item_record, app, barcode):
        itemData = extractItemData(item_record)
        last_copies.append(itemData)
        pd.DataFrame(last_copies).to_csv(PARTIAL_FILE, index=False)

    with open(DONE_FILE, 'a') as f:
        f.write(barcode + '\n')

if not last_copies:
    print("No last copies")
    item_search.close()
    os.remove(DONE_FILE)
    exit()

df = pd.DataFrame(last_copies)

for selector in [SELECTOR_NAMES]:
    selector_df = df[df['Selector'] == selector]
    if len(selector_df) > 0:
        filename = f"CSV/{selector}_last_copies_{time.strftime('%Y%m%d')}.csv"
        selector_df.to_csv(filename, index=False)
        print(f"Saved {len(selector_df)} items to {filename}")
    else:
        print(f"No items for {selector}")

print("\nCleaning up...")
item_search.close()
os.remove(DONE_FILE)
if os.path.exists(PARTIAL_FILE):
    os.remove(PARTIAL_FILE)
print("Done")
