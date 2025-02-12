import requests
import pandas as pd

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    
    # Select the relevant columns
    df = df[['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'price_change_percentage_24h']]
    return df

crypto_data = fetch_crypto_data()
print(crypto_data.head())
def analyze_data(df):
    # Top 5 cryptocurrencies by market cap
    top_5 = df[['name', 'symbol', 'market_cap']].sort_values(by='market_cap', ascending=False).head(5)
    
    # Average price of top 50 cryptocurrencies
    avg_price = df['current_price'].mean()
    
    # Highest and lowest 24-hour price change
    highest_change = df.loc[df['price_change_percentage_24h'].idxmax()]
    lowest_change = df.loc[df['price_change_percentage_24h'].idxmin()]
    
    return top_5, avg_price, highest_change, lowest_change

top_5, avg_price, highest_change, lowest_change = analyze_data(crypto_data)

print("Top 5 Cryptocurrencies by Market Cap:\n", top_5)
print("\nAverage Price of Top 50 Cryptocurrencies:", avg_price)
print("\nHighest 24-Hour Price Change:\n", highest_change)
print("\nLowest 24-Hour Price Change:\n", lowest_change)
import openpyxl
import time

def create_excel(df, filename="crypto_data.xlsx"):
    # Create a new Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Crypto Data"
    
    # Define headers
    headers = ['Name', 'Symbol', 'Current Price (USD)', 'Market Cap', '24h Volume', 'Price Change (24h)']
    ws.append(headers)
    
    # Add the data
    for index, row in df.iterrows():
        ws.append([row['name'], row['symbol'], row['current_price'], row['market_cap'], row['total_volume'], row['price_change_percentage_24h']])
    
    # Save the file
    wb.save(filename)

def update_excel_periodically():
    while True:
        crypto_data = fetch_crypto_data()
        create_excel(crypto_data)
        print("Excel updated with latest data.")
        time.sleep(300)  # Wait for 5 minutes

update_excel_periodically()

