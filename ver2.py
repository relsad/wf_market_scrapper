import csv
import requests

# Function to get price from the API
def get_price_from_api(augment_name):
    url = f"https://api.warframe.market/v1/items/{augment_name}/orders"  # API endpoint to get orders
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            # Extract price from the response (change according to actual API response structure)
            # Here, we're assuming it returns the price in a list under 'payload' -> 'orders'
            if data['payload']['orders']:
                return data['payload']['orders'][0]['platinum']  # Assuming the first order is the most relevant
        except (KeyError, IndexError):
            print(f"Error processing data for {augment_name}")
    return 0  # Default price if API fails or no orders are found

# Read the CSV file
with open('augment_mods.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Update the price for each augment mod
for row in rows:
    augment_name = row['Augment Mod Name'].lower().replace(" ", "_")
    price = get_price_from_api(augment_name)
    row['Price'] = price

# Write the updated data back to the CSV
with open('updated_augment_mods.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Augment Mod Name', 'Favored Syndicates', 'Price']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(rows)

print("CSV updated successfully!")
