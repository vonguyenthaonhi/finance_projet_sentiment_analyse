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
        merged_data = pd.merge(financial_data, ratios_data[['Date', 'Ratio Value']], on='Date', how='inner')
        #merged_data['Ratio Value'].fillna(0, inplace=True)
        merged_data["Ratio Value"] = merged_data["Ratio Value"].fillna(0) 
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
        merged_data = pd.merge(financial_data, ratios_data[['Date', 'Dernier']], on='Date', how='inner')
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


def add_rfr(financial_data_path, rfr_path, output_dir, company_name):
    """
    Adds the Risk_free rate from the ratios file to the financial data file, ensuring alignment by date.
    """
    try:
        financial_data = pd.read_csv(financial_data_path)
        rfr_data = pd.read_csv(rfr_path, index_col=0)
        rfr_data['Date'] = pd.to_datetime(rfr_data['Date'])
        financial_data['Date'] = pd.to_datetime(financial_data['Date'])

        # Ensure both datasets have the necessary columns
        rfr_data = rfr_data[['Date', 'Close']]
        rfr_data.rename(columns={'Close': 'Risk-free rate'}, inplace=True)
        merged_data = pd.merge(financial_data, rfr_data, on='Date', how='left')

        sanitized_company_name = company_name.replace(' ', '_')
        output_file = os.path.join(output_dir, f"{sanitized_company_name}_add_risk_free_rate.csv")
        merged_data.to_csv(output_file, index=False)

        print(f"Risk-free rate added successfully. Updated file saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

add_rfr('new_data/financial_data_putcall/BP_PLC_updated_financial_data.csv', 'new_data/volatility/risk_free_rate_EU.csv', 'new_data/risk_free_rate_added', 'BP PLC')
add_rfr('new_data/financial_data_putcall/Stora_Enso_updated_financial_data.csv', 'new_data/volatility/risk_free_rate_EU.csv', 'new_data/risk_free_rate_added', 'Stora Enso')
add_rfr('new_data/financial_data_putcall/Total_Energies_updated_financial_data.csv', 'new_data/volatility/risk_free_rate_EU.csv', 'new_data/risk_free_rate_added', 'Total Energies')
add_rfr('new_data/financial_data_putcall/FMC_Corp_updated_financial_data.csv', 'new_data/volatility/risk_free_rate_US.csv', 'new_data/risk_free_rate_added', 'FMC Corp')
add_rfr('new_data/financial_data_putcall/BHP_Group_updated_financial_data.csv', 'new_data/volatility/risk_free_rate_US.csv', 'new_data/risk_free_rate_added', 'BHP Group')