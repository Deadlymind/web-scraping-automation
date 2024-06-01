import requests
from bs4 import BeautifulSoup as bs
import logging
import argparse
import re
import csv
from datetime import datetime
from time import sleep
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cache for storing conversion results within a session
conversion_cache = defaultdict(dict)

def is_valid_currency_code(currency_code):
    return bool(re.match(r'^[A-Za-z]{3}$', currency_code))

def get_currency(in_currency, out_currency, amount, retries=3, backoff=1.0):
    # Check cache first
    if in_currency in conversion_cache and out_currency in conversion_cache[in_currency] and amount in conversion_cache[in_currency][out_currency]:
        logging.info(f"Using cached result for {amount} {in_currency} to {out_currency}")
        return conversion_cache[in_currency][out_currency][amount]

    url = f"https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount={amount}"
    for attempt in range(retries):
        try:
            logging.info(f"Fetching data from URL: {url} (Attempt {attempt + 1}/{retries})")
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            soup = bs(response.text, "html.parser")
            currency_element = soup.find("span", class_="ccOutputRslt")
            
            if currency_element:
                conversion_result = currency_element.get_text().split()[0]
                logging.info(f"Conversion result: {conversion_result}")
                # Cache the result
                if in_currency not in conversion_cache:
                    conversion_cache[in_currency] = {}
                if out_currency not in conversion_cache[in_currency]:
                    conversion_cache[in_currency][out_currency] = {}
                conversion_cache[in_currency][out_currency][amount] = conversion_result
                return conversion_result
            else:
                logging.error(f"Could not find conversion result on the page for {in_currency} to {out_currency}.")
                return None

        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            if attempt < retries - 1:
                sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                return None
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

def main(in_currency=None, out_currency=None, amounts=None, output_file=None):
    while not in_currency or not is_valid_currency_code(in_currency):
        in_currency = input("Enter the input currency code (e.g., USD): ").upper()
        if not is_valid_currency_code(in_currency):
            logging.error("Invalid input currency code. Please enter a 3-letter currency code.")

    while not out_currency or not is_valid_currency_code(out_currency):
        out_currency = input("Enter the output currency code (e.g., EUR): ").upper()
        if not is_valid_currency_code(out_currency):
            logging.error("Invalid output currency code. Please enter a 3-letter currency code.")

    if not amounts:
        amounts_input = input("Enter the amounts to be converted (comma-separated): ")
        amounts = amounts_input.split(',')

    try:
        amounts = [float(amount.strip()) for amount in amounts]
    except ValueError:
        logging.error("Invalid amount entered. Please enter numeric values.")
        return

    results = []
    for amount in amounts:
        result = get_currency(in_currency, out_currency, amount)
        if result:
            results.append((amount, in_currency, result, out_currency))

    if results:
        if not output_file:
            output_file = f"currency_conversions_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amount', 'From Currency', 'Converted Amount', 'To Currency'])
            writer.writerows(results)
        logging.info(f"Results saved to {output_file}")
        for result in results:
            print(f"{result[0]} {result[1]} = {result[2]} {result[3]}")
    else:
        print("Failed to retrieve any conversion results.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Currency converter")
    parser.add_argument("in_currency", nargs='?', help="The input currency code (e.g., USD)")
    parser.add_argument("out_currency", nargs='?', help="The output currency code (e.g., EUR)")
    parser.add_argument("amounts", nargs='*', help="The amounts to be converted (space-separated)")
    parser.add_argument("--output", help="Output file to save the results")
    args = parser.parse_args()

    main(args.in_currency, args.out_currency, args.amounts, args.output)
