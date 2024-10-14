import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from itertools import combinations
from multiprocessing import Pool, cpu_count


# ticker = "AAPL"

# def convert(unix_msec):
#     # Convert milliseconds to seconds
#     unix_sec = unix_msec / 1000
#     # Convert to datetime object
#     dt = datetime.fromtimestamp(unix_sec)
#     # Format to YYYY-MM-DD-HH-MM
#     formatted_time = dt.strftime('%Y-%m-%d-%H-%M')
#     return formatted_time

# # List Aggregates (Bars)
# data = []
# for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-12-31", to="2024-06-01", limit=50000):
#     data.append(a)
# # Sample input data: Replace this with actual data

# # Function to extract relevant data
# def extract_data(data):
#     extracted_data = []
#     for agg in data:
#         extracted_data.append({
#             'timestamp': convert(agg.timestamp),
#             'close': agg.close,
#             'volume': agg.volume,
#         })
#     return extracted_data

# def filter_data_by_timeframe(data):
#     filtered_data = []
#     for entry in data:
#         # Parse the timestamp
#         timestamp = entry['timestamp']
#         dt = datetime.strptime(timestamp, '%Y-%m-%d-%H-%M')

#         # Extract the time component
#         entry_time = dt.time()

#         # Check if the time is within the specified timeframe
#         if datetime.strptime('14:00', '%H:%M').time() <= entry_time <= datetime.strptime('15:00', '%H:%M').time() or entry_time == datetime.strptime('8:30', '%H:%M').time():
#             filtered_data.append(entry)

#     return filtered_data

# def create_csv_with_trading_data(data, output_filename):
#     # Convert timestamp to datetime and add to data entries
#     for entry in data:
#         entry['datetime'] = datetime.strptime(entry['timestamp'], '%Y-%m-%d-%H-%M')

#     # Create DataFrame
#     df = pd.DataFrame(data)

#     # Sort data by datetime
#     df = df.sort_values(by='datetime').reset_index(drop=True)

#     # Function to insert blank and date rows
#     def insert_blank_and_date_rows(df):
#         new_data = []
#         previous_date = None
#         for i, row in df.iterrows():
#             current_date = row['datetime'].date()
#             if previous_date and previous_date != current_date:
#                 # Insert a blank row and a date row
#                 new_data.append({'timestamp': '', 'close': '', 'volume': '', 'datetime': None})
#                 new_data.append({'timestamp': f'Date: {current_date}', 'close': '', 'volume': '', 'datetime': None})
#             new_data.append(row.to_dict())
#             previous_date = current_date
#         return new_data

#     # Insert blank and date rows
#     new_data = insert_blank_and_date_rows(df)

#     # Convert new_data back to DataFrame
#     result_df = pd.DataFrame(new_data)

#     # Select relevant columns
#     result_df = result_df[['timestamp', 'close', 'volume']]

#     # Save to CSV
#     result_df.to_csv(output_filename, index=False)

#     return result_df





# data1 = extract_data(data)
# data= filter_data_by_timeframe(data1)
# # Extract data

# create_csv_with_trading_data(data, 'output.csv')

# print(data)

# #we need to filter the data to just the last hour of a trading day: 14:00-15:00



# # Example usage

# # Convert to DataFrame



import yfinance as yf
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

# List of 50 stock pairs formatted for yfinance
pairs = [
    ('AAPL', 'MSFT'), ('JPM', 'BAC'), ('KO', 'PEP'), ('XOM', 'CVX'), 
    ('VZ', 'T'), ('WMT', 'TGT'), ('PFE', 'MRK'), ('COST', 'WMT'),
    ('DIS', 'CMCSA'), ('CVS', 'WBA'), ('GS', 'MS'), ('UNH', 'ANTM'),
    ('BA', 'LMT'), ('V', 'MA'), ('AAL', 'DAL'), ('NFLX', 'DIS'),
    ('F', 'GM'), ('CSCO', 'JNPR'), ('C', 'JPM'), ('HON', 'UTX'),
    ('ABT', 'MDT'), ('INTC', 'AMD'), ('NKE', 'LULU'), ('TSLA', 'F'),
    ('GILD', 'AMGN'), ('AIG', 'PRU'), ('LOW', 'HD'), ('MO', 'PM'),
    ('WFC', 'USB'), ('MDLZ', 'KHC'), ('GD', 'NOC'), ('LUV', 'ALK'),
    ('TMO', 'DHR'), ('CAT', 'DE'), ('MSFT', 'GOOGL'), ('FB', 'TWTR'),
    ('SBUX', 'MCD'), ('AAPL', 'NVDA'), ('CVX', 'COP'), ('BK', 'STT'),
    ('DUK', 'SO'), ('D', 'EXC'), ('TXN', 'QCOM'), ('BMY', 'LLY'),
    ('PNC', 'USB'), ('EBAY', 'AMZN'), ('ADP', 'PAYX'), ('GD', 'RTX'),
    ('EXPE', 'BKNG'), ('MMM', 'HON')
]

# Function to download the adjusted close prices for each pair
def download_pair_data(pair):
    stock1, stock2 = pair
    try:
        # Download adjusted close price data for both stocks in the pair
        stock1_data = yf.download(stock1, start="2019-01-01", end="2024-01-01")['Adj Close']
        stock2_data = yf.download(stock2, start="2019-01-01", end="2024-01-01")['Adj Close']
        
        # Return the concatenated data
        return pd.concat([stock1_data, stock2_data], axis=1, keys=[stock1, stock2]).dropna()
    except Exception as e:
        print(f"Error downloading data for {pair}: {e}")
        return None

# Function to test cointegration
def test_cointegration(data, pair):
    stock1, stock2 = pair
    try:
        score, p_value, _ = coint(data[stock1], data[stock2])
        if p_value < 0.05:
            print(f"Cointegrated pair: {stock1} and {stock2}, p-value: {p_value}")
            return (stock1, stock2, p_value)
    except Exception as e:
        print(f"Error testing cointegration for {pair}: {e}")
    return None

# List to store cointegrated pairs
cointegrated_pairs = []

# Iterate over each pair and test for cointegration
for pair in pairs:
    data = download_pair_data(pair)
    if data is not None and len(data) > 100:  # Make sure there's enough data
        result = test_cointegration(data, pair)
        if result:
            cointegrated_pairs.append(result)

# Show cointegrated pairs
print("\nCointegrated pairs found:")
for pair in cointegrated_pairs:
    print(pair)

# ('GS', 'MS', 0.04186714636782074)
# ('V', 'MA', 0.007841552071482535)
# ('AAL', 'DAL', 0.04447909779373223)
# ('MO', 'PM', 0.005271338520811497)
# ('MDLZ', 'KHC', 0.0287969486347407)