import os
import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    """
    Load and preprocess the dataset.
    
    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    # Load the dataset
    data = pd.read_csv(file_path)

    # Convert 'Date' to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Define PCR thresholds for sentiment classification
    def classify_pcr(pcr):
        if pcr < 0.7:
            return 'Bullish'
        elif pcr > 1.2:
            return 'Bearish'
        else:
            return 'Neutral'

    data['PCR Sentiment'] = data['Put-Call Ratio'].apply(classify_pcr)

    # Check for consecutive signals
    data['Consecutive Signal'] = (data['PCR Sentiment'] != data['PCR Sentiment'].shift()).cumsum()
    data['Signal Streak'] = data.groupby('Consecutive Signal').cumcount() + 1

    # Assign initial equal weights (20% for each stock)
    initial_weight = 0.2
    data['Initial Weight'] = initial_weight

    # Adjust weights based on sentiment classification and streak length
    def adjust_weights(row):
        if row['PCR Sentiment'] == 'Bullish':
            return row['Initial Weight'] + 0.05 * min(row['Signal Streak'], 3)  # Increase weight up to 15% for 3 days
        elif row['PCR Sentiment'] == 'Bearish':
            return row['Initial Weight'] - 0.05 * min(row['Signal Streak'], 3)  # Decrease weight up to 15% for 3 days
        else:
            return row['Initial Weight']  # No change for Neutral

    data['Adjusted Weight'] = data.apply(adjust_weights, axis=1)

    # Normalize weights to ensure they sum to 100%
    total_adjusted_weight = data['Adjusted Weight'].sum()
    data['Normalized Weight'] = data['Adjusted Weight'] / total_adjusted_weight

    # Calculate portfolio returns
    data['Portfolio Return'] = data['Daily Return'] * data['Normalized Weight']

    return data

def calculate_var_and_sharpe(data):
    """
    Calculate Value at Risk (VaR) and Sharpe Ratio.

    Parameters:
        data (pd.DataFrame): Dataset with 'Portfolio Return'.

    Returns:
        dict: VaR and Sharpe Ratio.
    """
    # Value at Risk (VaR)
    confidence_level = 0.95
    portfolio_returns = data['Portfolio Return']
    VaR_95 = np.percentile(portfolio_returns, (1 - confidence_level) * 100)

    # Sharpe Ratio
    risk_free_rate = 0.02 / 252  # Assuming annual risk-free rate of 2%
    mean_portfolio_return = portfolio_returns.mean()
    portfolio_std_dev = portfolio_returns.std()

    sharpe_ratio = (mean_portfolio_return - risk_free_rate) / portfolio_std_dev

    return {
        'VaR_95': VaR_95,
        'Sharpe Ratio': sharpe_ratio
    }

def process_directory(directory_path, output_dir):
    """
    Process all CSV files in a directory and save updated data to output directory.

    Parameters:
        directory_path (str): Path to the directory containing CSV files.
        output_dir (str): Path to the directory to save updated files.

    Returns:
        dict: Results for each file.
    """
    results = {}
    all_data = []
    stock_names = []

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            
            # Load and preprocess data
            data = load_and_preprocess_data(file_path)

            # Calculate VaR and Sharpe Ratio for individual stocks
            metrics = calculate_var_and_sharpe(data)

            # Store results for individual stocks
            results[file_name] = metrics

            # Collect data for the entire portfolio
            stock_name = os.path.splitext(file_name)[0]  # Extract company name from file name
            stock_names.extend([stock_name] * len(data))
            all_data.append(data[['Date', 'Portfolio Return', 'Normalized Weight']].copy())

            # Export the updated dataset
            sanitized_company_name = stock_name.replace(' ', '_')
            output_file = os.path.join(output_dir, f"{sanitized_company_name}_updated_financial_data.csv")
            data.to_csv(output_file, index=False)

            print(f"File processed: {file_name}. Updated file saved to: {output_file}")

    # Combine data for the entire portfolio
    portfolio_data = pd.concat(all_data, axis=0)
    portfolio_data['Stock'] = stock_names

    # Calculate portfolio-level VaR and Sharpe Ratio
    portfolio_metrics = calculate_var_and_sharpe(portfolio_data)

    # Calculate overall weight per stock
    total_weights = portfolio_data.groupby('Stock')['Normalized Weight'].sum()
    portfolio_metrics['Stock Weights'] = total_weights.to_dict()

    return results, portfolio_metrics
# Define the input and output directory paths
input_folder = "new_data/financial_data_putcall"  # Replace with your actual input folder path
output_folder = "new_data/portefeuille_data"  # Replace with your actual output folder path

# Process the directory and calculate metrics
results, portfolio_metrics = process_directory(input_folder, output_folder)


# Print overall portfolio metrics
print("\nPortfolio-Level Metrics:")
print(f"VaR (95%): {portfolio_metrics['VaR_95']}")
print(f"Sharpe Ratio: {portfolio_metrics['Sharpe Ratio']}")
print(f"Stock Weights: {portfolio_metrics['Stock Weights']}")
