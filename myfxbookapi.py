import requests
import csv

session = 'lTVPIoLWBnjsDDjG8AQy2661187'


def fetch_data(session):
    symbols = None
    try:
        response = requests.get(f'https://www.myfxbook.com/api/get-community-outlook.json?session={session}')
        response.raise_for_status()
        symbols = response.json()['symbols']
    except requests.exceptions.RequestException as error:
        # handle errors here
        print(error)

    return symbols


def write_to_csv(data, filename="output.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Assuming the data is a list of dictionaries
        # Write the header (keys from the first dictionary)
        writer.writerow(data[0].keys())
        
        # Write the data
        for item in data:
            writer.writerow(item.values())


if __name__ == "__main__":
    fetched_symbols = fetch_data(session)
    if fetched_symbols:
        write_to_csv(fetched_symbols)
        print(f"Data written to output.csv")
    else:
        print("Failed to fetch symbols")
