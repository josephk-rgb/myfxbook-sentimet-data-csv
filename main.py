import requests
import csv
from datetime import datetime, timedelta, timezone
import smtplib
from email.message import EmailMessage

# API session and output file
session = 'lTVPIoLWBnjsDDjG8AQy2661187'
OUTPUT_FILE = 'output.csv'

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'   # replace with your email
SENDER_PASSWORD = 'your_password'      # replace with your password or use an app-specific password
RECIPIENT_EMAIL = 'recipient_email@gmail.com'  # replace with the recipient's email


def is_forex_market_open():
    # Define the Eastern Time Zone (ET)
    ET = timezone(timedelta(hours=-5))  # For Eastern Standard Time. Adjust for Daylight Saving Time if needed.

    # Get the current time in ET
    current_time_et = datetime.now(ET)

    # Market opens at 5:00 pm ET on Sunday and closes at 5:00 pm ET on Friday
    market_open_time = current_time_et.replace(hour=17, minute=0, second=0, microsecond=0)
    
    # Check if current time is within the forex market hours
    if current_time_et.weekday() == 6 and current_time_et < market_open_time:
        return False  # Sunday before 5:00 pm ET
    if current_time_et.weekday() == 4 and current_time_et >= market_open_time:
        return False  # Friday after 5:00 pm ET
    if current_time_et.weekday() == 5:
        return False  # All of Saturday

    return True  # Market is open

def fetch_data(session):
    symbols = None
    try:
        response = requests.get(f'https://www.myfxbook.com/api/get-community-outlook.json?session={session}')
        response.raise_for_status()
        symbols = response.json()['symbols']
    except requests.exceptions.RequestException as error:
        send_email(f"Error fetching data: {error}")
        print(error)
    return symbols



def append_to_csv(data, filename=OUTPUT_FILE):
    # Check if the file exists to determine if headers are needed
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # If file doesn't exist, write headers
        if not file_exists:
            headers = ['timestamp', 'name', 'shortPercentage', 'longPercentage', 
                       'shortVolume', 'longVolume', 'longPositions', 
                       'shortPositions', 'totalPositions', 'avgShortPrice', 'avgLongPrice']
            writer.writerow(headers)

        # Write the data with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for item in data:
            row = [timestamp] + list(item.values())
            writer.writerow(row)


def send_email(error_message):
    msg = EmailMessage()
    msg.set_content(error_message)
    msg['Subject'] = 'Error in Data Collection Script'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == "__main__":
    if not is_forex_market_open():
        print("Forex market is closed. Script will not run.")
    else:
        try:
            fetched_symbols = fetch_data(session)
            if fetched_symbols:
                append_to_csv(fetched_symbols)
                print(f"Data appended to {OUTPUT_FILE}")
            else:
                print("Failed to fetch symbols")
        except Exception as e:
            send_email(f"Unexpected error in script: {e}")
            print(f"Unexpected error: {e}")
