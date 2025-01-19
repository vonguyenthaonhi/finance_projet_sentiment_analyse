import pandas as pd
import os

def merge_put_call_ratios(file_paths, stock_names):
    """
    Merges 'Put-Call Ratio' data for multiple stocks into a single DataFrame aligned by date.
    """
    stock_data = {name: pd.read_csv(file_path) for name, file_path in zip(stock_names, file_paths)}
    put_call_ratios = {name: df[['Date', 'Put-Call Ratio']] for name, df in stock_data.items()}
    merged_data = None

    for name, df in put_call_ratios.items():
        df = df.rename(columns={'Put-Call Ratio': name}) 
        merged_data = pd.merge(merged_data, df, on='Date', how='outer')

    merged_data['Date'] = pd.to_datetime(merged_data['Date'])
    merged_data.set_index('Date', inplace=True)

    return merged_data

def calculate_signals_pcr(put_call_ratios, bullish_threshold, bearish_threshold):
    """
    Define function to calculate signals based on Put-Call Ratio, with streak reset for trend changes.
    """
    streak = 0
    signals = []
    previous_signal = None

    for ratio in put_call_ratios:
        if ratio < bullish_threshold:  
            if previous_signal != "Bullish":
                streak = 0  # Reset streak on trend change
            streak += 1
            current_signal = "Bullish"
        elif ratio > bearish_threshold:  
            if previous_signal != "Bearish":
                streak = 0 
            streak -= 1
            current_signal = "Bearish"
        else:  # Neutral
            if previous_signal != "Neutral":
                streak = 0 
            current_signal = "Neutral"

        # Assign Buy, Sell, or Hold based on streak
        if streak >= 3:
            signals.append("Buy")
        elif streak <= -3:
            signals.append("Sell")
        else:
            signals.append("Hold")

        # Update previous signal
        previous_signal = current_signal

    return signals

def calculate_dynamic_portfolio_weights(signal_data, stock_names):
    """
    Calculates daily portfolio weights dynamically based on signal data for multiple stocks.
    """
    # Initialize portfolio weights
    initial_weight = 1 / len(stock_names)

    weight_data = pd.DataFrame(index=signal_data.index)

    # Calculate dynamic weights for each stock
    for stock in stock_names:
        weight_data[f"{stock}_Weight"] = initial_weight  
        for i, signal in enumerate(signal_data[f"{stock}_Signal"]):
            if i > 0:  
                if signal == "Buy":
                    weight_data.iloc[i, weight_data.columns.get_loc(f"{stock}_Weight")] = (
                        weight_data.iloc[i - 1, weight_data.columns.get_loc(f"{stock}_Weight")] * 1.1
                    )  # Increase by 10%
                elif signal == "Sell":
                    weight_data.iloc[i, weight_data.columns.get_loc(f"{stock}_Weight")] = (
                        weight_data.iloc[i - 1, weight_data.columns.get_loc(f"{stock}_Weight")] * 0.9
                    )  # Decrease by 10%
                else:
                    weight_data.iloc[i, weight_data.columns.get_loc(f"{stock}_Weight")] = (
                        weight_data.iloc[i - 1, weight_data.columns.get_loc(f"{stock}_Weight")]
                    )  # Hold

    # Normalize weights to ensure they sum to 1 each day
    weight_data["Total_Weight"] = weight_data[[f"{stock}_Weight" for stock in stock_names]].sum(axis=1)
    for stock in stock_names:
        weight_data[f"{stock}_Normalized_Weight"] = (
            weight_data[f"{stock}_Weight"] / weight_data["Total_Weight"]
        )

    weight_data.drop(columns=["Total_Weight"], inplace=True)

    return weight_data




#a mettre dans un fichier main...
file_paths = [
    "new_data/risk_free_rate_added/BHP_Group_add_risk_free_rate.csv",
    "new_data/risk_free_rate_added/BP_PLC_add_risk_free_rate.csv",
    "new_data/risk_free_rate_added/FMC_Corp_add_risk_free_rate.csv",
    "new_data/risk_free_rate_added/Stora_Enso_add_risk_free_rate.csv",
    "new_data/risk_free_rate_added/Total_Energies_add_risk_free_rate.csv"
]
stock_names = ["BHP_Group", "BP_PLC", "FMC_Corp", "Stora_Enso", "Total_Energies"]
merged_data = merge_put_call_ratios(file_paths, stock_names)

bullish_threshold = -1
bearish_threshold = 1

signal_data = merged_data.copy()
for stock in stock_names:
    signal_data[f"{stock}_Signal"] = calculate_signals_pcr(signal_data[stock], bullish_threshold, bearish_threshold)

weight_data = calculate_dynamic_portfolio_weights(signal_data, stock_names)
