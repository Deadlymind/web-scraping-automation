import requests
from datetime import datetime
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input():
    ticker = input("Enter the ticker symbol of the company: ")
    from_date = input("Enter the start date (yyyy-mm-dd or yyyy/mm/dd): ")
    to_date = input("Enter the end date (yyyy-mm-dd or yyyy/mm/dd): ")
    return ticker, from_date, to_date

def convert_to_epoch(date_str):
    for date_format in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            date_time = datetime.strptime(date_str, date_format)
            return int(time.mktime(date_time.timetuple()))
        except ValueError:
            continue
    logging.error(f"Error parsing date: {date_str} does not match expected formats")
    raise ValueError(f"Date format is incorrect: {date_str}")

def fetch_stock_data(ticker, from_epoch, to_epoch):
    url = (f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
        f"?period1={from_epoch}&period2={to_epoch}&interval=1d&events=history&includeAdjustedClose=true")
    headers = {
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36")
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        raise

def save_to_file(content, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(content)
        logging.info(f"Data saved to {filename}")
    except IOError as e:
        logging.error(f"Error saving file: {e}")
        raise

def main():
    try:
        ticker, from_date, to_date = get_user_input()
        from_epoch = convert_to_epoch(from_date)
        to_epoch = convert_to_epoch(to_date)

        logging.info(f"Fetching data for {ticker} from {from_date} to {to_date}")
        content = fetch_stock_data(ticker, from_epoch, to_epoch)

        filename = f"{ticker}.csv"
        save_to_file(content, filename)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
