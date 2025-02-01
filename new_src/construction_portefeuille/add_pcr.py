import os
import pandas as pd


class PutCallRatioAdder:
    """
    A class to add Put-Call Ratio data to financial datasets,
    ensuring alignment by date and filtering based on specific date ranges.
    """

    def __init__(self, output_dir):
        """
        Initializes the class with an output directory.
        
        :param output_dir: Directory where updated files will be saved.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def add_put_call_ratio_us(self, financial_data_path, ratios_path, company_name):
        """
        Adds the US Put-Call Ratio to financial data, aligning by date and filtering up to 31.01.2024.
        
        :param financial_data_path: Path to the financial data CSV file.
        :param ratios_path: Path to the US Put-Call Ratios CSV file.
        :param company_name: Name of the company for output file naming.
        """
        try:
            financial_data = pd.read_csv(financial_data_path)
            ratios_data = pd.read_csv(ratios_path)

            financial_data['Date'] = pd.to_datetime(financial_data['Date'])
            ratios_data['Date'] = pd.to_datetime(ratios_data['Date'])

            financial_data = financial_data[financial_data['Date'] <= '2024-01-31']
            ratios_data = ratios_data[ratios_data['Date'] <= '2024-01-31']

            merged_data = pd.merge(
                financial_data, ratios_data[['Date', 'Ratio Value']], on='Date', how='inner'
            )
            merged_data['Ratio Value'] = merged_data['Ratio Value'].fillna(0)
            merged_data.rename(columns={'Ratio Value': 'Put-Call Ratio'}, inplace=True)

            self._save_file(merged_data, company_name)

        except Exception as e:
            print(f"An error occurred: {e}")

    def add_put_call_ratio_eu(self, financial_data_path, ratios_path, company_name):
        """
        Adds the EU Put-Call Ratio to financial data, aligning by date and filtering between 07.10.2019 and 31.01.2024.
        
        :param financial_data_path: Path to the financial data CSV file.
        :param ratios_path: Path to the EU Put-Call Ratios CSV file.
        :param company_name: Name of the company for output file naming.
        """
        try:
            financial_data = pd.read_csv(financial_data_path)
            ratios_data = pd.read_csv(ratios_path)

            financial_data['Date'] = pd.to_datetime(financial_data['Date']).dt.strftime('%Y-%m-%d')
            ratios_data['Date'] = pd.to_datetime(
                ratios_data['Date'], format='%d/%m/%Y'
            ).dt.strftime('%Y-%m-%d')

            financial_data = financial_data[
                (financial_data['Date'] >= '2019-10-07') & (financial_data['Date'] <= '2024-01-31')
            ]
            ratios_data = ratios_data[
                (ratios_data['Date'] >= '2019-10-07') & (ratios_data['Date'] <= '2024-01-31')
            ]

            if ratios_data['Dernier'].dtype == 'object':
                ratios_data['Dernier'] = ratios_data['Dernier'].str.replace(',', '.').astype(float)

            merged_data = pd.merge(
                financial_data, ratios_data[['Date', 'Dernier']], on='Date', how='inner'
            )
            merged_data['Dernier'].fillna(0, inplace=True)
            merged_data.rename(columns={'Dernier': 'Put-Call Ratio'}, inplace=True)

            self._save_file(merged_data, company_name)

        except Exception as e:
            print(f"An error occurred: {e}")

    def _save_file(self, data, company_name):
        """
        Saves the processed data to a CSV file.
        
        :param data: DataFrame containing updated financial data.
        :param company_name: Name of the company for file naming.
        """
        sanitized_company_name = company_name.replace(' ', '_')
        output_file = os.path.join(self.output_dir, f"{sanitized_company_name}_updated_financial_data.csv")
        data.to_csv(output_file, index=False)
        print(f"Updated file saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    output_directory = "new_data/full_data"
    ratio_adder = PutCallRatioAdder(output_directory)

    ratio_adder.add_put_call_ratio_us(
        "new_data/stock_infos/FMC_Corp_financial_data.csv", 
        "new_data/webscrapped_call_put_ratio/ratios.csv", 
        "FMC Corp"
    )
    ratio_adder.add_put_call_ratio_us(
        "new_data/stock_infos/BHP_Group_financial_data.csv", 
        "new_data/webscrapped_call_put_ratio/ratios.csv", 
        "BHP Group"
    )
    ratio_adder.add_put_call_ratio_eu(
        "new_data/stock_infos/BP_PLC_financial_data.csv", 
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv", 
        "BP PLC"
    )
    ratio_adder.add_put_call_ratio_eu(
        "new_data/stock_infos/Stora_Enso_financial_data.csv", 
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv", 
        "Stora Enso"
    )
    ratio_adder.add_put_call_ratio_eu(
        "new_data/stock_infos/Total_Energies_financial_data.csv", 
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv", 
        "Total Energies"
    )
