import requests
import json
import csv
from datetime import datetime
import import_json

# Load JSON data using the function from the module
json_file_path = 'config.json'
config = import_json.load_json_data(json_file_path)


def address_selection():
    addresses_list = config.get("addresses", [])
    if not addresses_list:
        print("No addresses found.")
        return

    addresses = addresses_list[0]

    print("Select or manually enter an address:")

    for key in addresses:
        print(f"{key}: {addresses[key]}")
    select_address = input("Enter the key corresponding to the address you want to select, or (e)xit the script: ")
    if select_address in addresses:
        selected_address = addresses[select_address]
        print(f"You have selected the address: {selected_address}")
        return selected_address
    if (select_address[:2] == "0x") & (len(select_address) == 42):
        print(f"Proceeding with address: {select_address}")
        return select_address
    if select_address == "e":
        print("Script exiting")
        exit(0)
    else:
        print("Invalid entry. Please try again.")
        address_selection()


ethereum_address = address_selection()


def currency_selection():
    currencies_list = config.get("currencies", [])
    if not currencies_list:
        print("No currencies found. You may manually enter a symbol or (e)xit the script: ")

    currencies = currencies_list[0]

    print("Select or manually enter a currency:")

    for key in currencies:
        print(f"{key}: {currencies[key]}")
    select_currency = input("Enter the key corresponding to the currency you want to select, or (e)xit the script: ")

    if select_currency in currencies:
        select_currency = currencies[select_currency]
        print(f"You have selected the currency: {select_currency}")
        return select_currency
    if select_currency in ("e", "E", "q", "Q"):
        print("Script exiting")
        exit(0)
    else:
        print(f"You have input the currency: {select_currency}")
        return select_currency


currency_selection = currency_selection()


def payload_select(currency, offset=0, limit=100):
    query = json.dumps({
        "query": (
            "{\n  ethereum(network: ethereum) {\n    transfers(\n      options: {"
            f"offset: {offset}, "
            f"limit: {limit}}}\n      amount: {{}}\n"
            f"date: {{}}\n      any: [{{sender: {{is: \"{ethereum_address}\"}}}}, {{receiver:"
            f" {{is: \"{ethereum_address}\"}}}}]\n     currency: {{in: \"{currency}\"}}\n    ) {{\n      "
            f"transaction {{\n"
            f"   hash\n      }}\n      sender {{\n        address\n      }}\n      receiver {{\n        "
            f"address\n"
            f"  }}\n      currency {{\n        symbol\n        address\n      }}\n      amount(amountInUSD: "
            f"{{}},"
            f"currency: {{}})\n      block {{\n        timestamp {{\n          iso8601\n        }}\n      }}\n"
            f"}}\n  }}\n}}"
        ),
        "variables": "{}"
    })
    return query


def fetch_data_with_pagination(url, payload_func):
    all_data = []
    offset = 0
    limit = 100
    while True:
        payload = payload_func(currency_selection, offset, limit)
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': f'{config["api_key"]}',
            'Authorization': f'Bearer {config["token"]}'
        }
        response = requests.post(url, headers=headers, data=payload)
        try:
            response_data = response.json()
            transfers_data = response_data.get('data', {}).get('ethereum', {}).get('transfers', [])

            if not transfers_data:
                print("It looks like you don't have any more transactions.")
                print(f"Transaction returned: {transfers_data[:1]}")
                break

            all_data.extend(transfers_data)

        except json.decoder.JSONDecodeError as e:
            print("Error decoding JSON response:", e)
            print("Response content:", response.content)
            break
        
        offset += limit

    return all_data


# Define the path for the CSV file
current_datetime = datetime.now().strftime("%Y-%m-%d_%H%M%S")
address_end = ethereum_address[-4:]
csv_file_path = f"{address_end}_{currency_selection}_{current_datetime}.csv"

# Define the field names for the CSV file
field_names = ['timestamp', 'amount', 'currency_symbol', 'txhash', 'sender_address', 'receiver_address',
               'contract_address']

# Write data to the CSV file
data = fetch_data_with_pagination(config["url"], payload_select)
print(f"It looks like your transactions are empty: {len(data)}")
print(f"Aborting operation")

if not data:
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
      
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for transfer in data:
            writer.writerow({
                'timestamp': transfer['block']['timestamp']['iso8601'][:10],  # Write the first ten characters of timestamp
                'amount': "{:.2f}".format(float(transfer['amount'])),  # Format amount rounded to two decimal places
                'currency_symbol': transfer['currency']['symbol'],
                'txhash': transfer['transaction']['hash'],
                'sender_address': transfer['sender']['address'],
                'receiver_address': transfer['receiver']['address'],
                'contract_address': transfer['currency']['address'],
            })
        
        print(f"CSV file '{csv_file_path}' has been created successfully.")