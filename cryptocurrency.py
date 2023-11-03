import requests
import csv
import time

while True:
    # URL of the CoinGecko API endpoint to get cryptocurrency data
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',  # You can change the currency if needed
        'order': 'market_cap_desc',
        'per_page': 10,  # Number of cryptocurrencies to retrieve
        'page': 1,
        'sparkline': False,
    }

    # Send a GET request to the CoinGecko API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        crypto_data = response.json()
        
        # Create a list to store the cryptocurrency data
        crypto_list = []
        
        # Extract relevant information and store it in the list
        for crypto in crypto_data:
            crypto_name = crypto['name']
            crypto_symbol = crypto['symbol']
            crypto_price = crypto['current_price']
            market_cap = crypto['market_cap']
            volume_24h = crypto['total_volume']
            circulating_supply = crypto['circulating_supply']
            change_24h = crypto['price_change_percentage_24h']
            
            crypto_list.append([crypto_name, crypto_symbol, crypto_price, market_cap, volume_24h, circulating_supply, change_24h])
        
        # Write the cryptocurrency data to a CSV file
        with open('cryptocurrency_live_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(['Name', 'Symbol', 'Price (USD)', 'Market Cap (USD)', '24h Volume (USD)', 'Circulating Supply', 'Change (24h)'])
            # Write data rows
            csv_writer.writerows(crypto_list)
        
        print('Data has been saved to cryptocurrency_live_data.csv')
    else:
        print('Failed to retrieve data from CoinGecko API')

    # Wait for 1 minute before scraping again
    time.sleep(60)
