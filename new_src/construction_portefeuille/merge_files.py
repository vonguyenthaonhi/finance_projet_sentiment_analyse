import os
import pandas as pd

def add_put_call_ratio_us(financial_data_path, ratios_path, output_dir, company_name):
    """
    Adds the Put-Call Ratio US from the ratios file to the financial data file, ensuring alignment by date.
    """
    try:
        financial_data = pd.read_csv(financial_data_path)
        ratios_data = pd.read_csv(ratios_path)

        # Convert 'Date' columns to datetime for alignment
        financial_data['Date'] = pd.to_datetime(financial_data['Date'])
        ratios_data['Date'] = pd.to_datetime(ratios_data['Date'])

        # Merge the data on 'Date', assigning 0 to missing Put-Call Ratios in financial data
        merged_data = pd.merge(financial_data, ratios_data[['Date', 'Ratio Value']], on='Date', how='left')
        merged_data['Ratio Value'].fillna(0, inplace=True)
        merged_data.rename(columns={'Ratio Value': 'Put-Call Ratio'}, inplace=True)

        sanitized_company_name = company_name.replace(' ', '_')
        output_file = os.path.join(output_dir, f"{sanitized_company_name}_updated_financial_data.csv")
        merged_data.to_csv(output_file, index=False)

        print(f"Put-Call Ratio added successfully. Updated file saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

def add_put_call_ratio_eu(financial_data_path, ratios_path, output_dir, company_name):
    """
    Adds the Put-Call Ratio EU from the ratios file to the financial data file, ensuring alignment by date.
    """
    try:
        financial_data = pd.read_csv(financial_data_path)
        ratios_data = pd.read_csv(ratios_path)

        # Convert 'Date' columns to datetime with consistent format for alignment
        financial_data['Date'] = pd.to_datetime(financial_data['Date']).dt.strftime('%Y-%m-%d')
        ratios_data['Date'] = pd.to_datetime(ratios_data['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

        if ratios_data['Dernier'].dtype == 'object':
            ratios_data['Dernier'] = ratios_data['Dernier'].str.replace(',', '.').astype(float)

        # Merge the data on 'Date', assigning 0 to missing values in the financial data
        merged_data = pd.merge(financial_data, ratios_data[['Date', 'Dernier']], on='Date', how='left')
        merged_data['Dernier'].fillna(0, inplace=True)
        merged_data.rename(columns={'Dernier': 'Put-Call Ratio'}, inplace=True)

        sanitized_company_name = company_name.replace(' ', '_')
        output_file = os.path.join(output_dir, f"{sanitized_company_name}_updated_financial_data.csv")
        merged_data.to_csv(output_file, index=False)

        print(f"Column 'Dernier' added successfully. Updated file saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


add_put_call_ratio_us('new_data/volatility/FMC_Corp_financial_data_23k.csv', 'new_data/webscrapped_call_put_ratio/ratios.csv', 'new_data/financial_data_putcall', 'FMC Corp')
add_put_call_ratio_us('new_data/volatility/BHP_Group_financial_data_23k.csv', 'new_data/webscrapped_call_put_ratio/ratios.csv', 'new_data/financial_data_putcall', 'BHP Group')
add_put_call_ratio_eu('new_data/volatility/BP_PLC_financial_data_23k.csv', 'new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv', 'new_data/financial_data_putcall', 'BP PLC')
add_put_call_ratio_eu('new_data/volatility/Stora_Enso_financial_data_23k.csv', 'new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv', 'new_data/financial_data_putcall', 'Stora Enso')
add_put_call_ratio_eu('new_data/volatility/Total_Energies_financial_data_23k.csv', 'new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv', 'new_data/financial_data_putcall', 'Total Energies')

