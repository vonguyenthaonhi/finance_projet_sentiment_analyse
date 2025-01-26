import numpy as np
import pandas as pd
from polygon import RESTClient
from datetime import datetime, timedelta
from crontab import CronTab
import time


client = RESTClient(api_key="BHkwhucAhqNI8vu68aekkH_KeP1wbGVW")

underlying_stocks = ['BHP', 'FMC']  # liste des stocks
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

def get_put_call_ratio(underlying_stock, start_date, end_date):
    time.sleep(60)
    active_contracts = []
    for option in client.list_options_contracts(underlying_ticker=underlying_stock,
                                                expiration_date_gte=start_date,
                                                limit=1000):
        active_contracts.append(option)
        if len(active_contracts) % 5000 == 0:
            time.sleep(60)

    time.sleep(60)
    expired_contracts = []
    for option in client.list_options_contracts(underlying_ticker=underlying_stock,
                                                expiration_date_gte=start_date,
                                                limit=1000,
                                                expired=True):
        expired_contracts.append(option)
        if len(expired_contracts) % 5000 == 0:
            time.sleep(60)

    # conbiner les contrats actifs et expirés
    options_contracts = expired_contracts + active_contracts
    print(f"Total Contracts for {underlying_stock}: {len(options_contracts)}")

    df_list = []
    time.sleep(60)
    for i, contract in enumerate(options_contracts):
        df_list.append(pd.DataFrame(client.list_aggs(ticker=contract.ticker, multiplier=1, timespan='day', from_=start_date, to=end_date, limit=5000)).assign(ticker=contract.ticker))
        if i % 100 == 0:
            print(f"Getting data for contract {i} of {len(options_contracts)}")
        if len(df_list) % 5 == 0:
            time.sleep(60)

    time.sleep(60)
    # Combine la liste dans un data frame
    df = pd.concat(df_list)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # merge avec les contrats pour obtenir les contrats type
    df = pd.DataFrame(options_contracts).merge(df, on='ticker')

    # Calcul le put call ratio journalier
    df['call_volume'] = np.where(df['contract_type'] == 'call', df['volume'], 0)
    df['put_volume'] = np.where(df['contract_type'] == 'put', df['volume'], 0)
    df_grouped = df.groupby('timestamp')[['put_volume', 'call_volume', 'volume']].sum()
    df_grouped['put_call_ratio'] = df_grouped['put_volume'] / df_grouped['call_volume']

    return df_grouped

# excecute pour la journée et concatène
for stock in underlying_stocks:
    output_file = f'../../new_data/daily_put_call/daily_put_call_{stock}.csv'
    try:
        # Load existing data if file exists
        existing_data = pd.read_csv(output_file)
        existing_data['timestamp'] = pd.to_datetime(existing_data['timestamp'])
    except FileNotFoundError:
        # If the file doesn't exist, create an empty dataframe
        existing_data = pd.DataFrame(columns=['timestamp', 'put_volume', 'call_volume', 'volume', 'put_call_ratio'])

    df_grouped = get_put_call_ratio(stock, start_date, end_date)

    # Concatenate new data with existing data
    updated_data = pd.concat([existing_data, df_grouped]).drop_duplicates().sort_values('timestamp')
    updated_data.to_csv(output_file, index=False)



#Sur linux
# cron = CronTab(user="root")
# job = cron.new(command='python3 .\put_call_ratio_with_contratcs.py', comment='Daily Put-Call Ratio Calculation for Multiple Stocks')
# job.setall('0 0 * * *')  # Run daily at midnight
# cron.write()
# crontab -r
#crontab -e
#crontab -l
