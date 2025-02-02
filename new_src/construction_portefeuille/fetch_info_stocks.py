import yfinance as yf
import pandas as pd


class FinancialDataFetcher:
    """
    A class to fetch financial data for given stock symbols over a specified date range.
    """

    def __init__(self, symbols, start_date, end_date):
        """
        Initialize the FinancialDataFetcher with stock symbols and date range.

        :param symbols: Dictionary of company names and their stock symbols
        :param start_date: Start date for fetching data (YYYY-MM-DD)
        :param end_date: End date for fetching data (YYYY-MM-DD)
        """
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date

    def get_financial_data(self, symbol):
        """
        Fetch financial data for a given stock symbol.

        :param symbol: Stock symbol to fetch data for
        :return: DataFrame containing 'Close' prices and 'Daily Return' values
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(start=self.start_date, end=self.end_date)

            if data.empty:
                return None

            if data["Close"].isnull().any():
                print(f"Des valeurs manquantes trouvées dans 'Close' pour {symbol}")

            data["Daily Return"] = data["Close"].pct_change()

            if pd.isna(data["Daily Return"].iloc[0]):
                data.at[data.index[0], "Daily Return"] = 0.0

            return data[["Close", "Daily Return"]]

        except Exception as e:
            print(f"Erreur avec {symbol}: {e}")
            return None

    def export_to_csv(self, output_folder="new_data/stock_infos"):
        """
        Fetch and save financial data for all symbols in CSV format.

        :param output_folder: Directory where CSV files should be saved
        """
        for company, symbol in self.symbols.items():
            data = self.get_financial_data(symbol)
            if data is not None:
                data.index = data.index.strftime("%Y-%m-%d")
                file_name = (
                    f"{output_folder}/{company.replace(' ', '_')}_financial_data.csv"
                )
                data.to_csv(file_name, index=True)
                print(f"Fichier CSV généré pour {company} : {file_name}")
            else:
                print(f"Aucune donnée disponible pour {company}.")


if __name__ == "__main__":
    SYMBOLS = {
        "Total Energies": "TTE.PA",
        "FMC Corp": "FMC",
        "BP PLC": "BP",
        "Stora Enso": "STE",
        "BHP Group": "BHP",
    }

    START_DATE = "2019-01-01"
    END_DATE = "2024-12-31"

    fetcher = FinancialDataFetcher(SYMBOLS, START_DATE, END_DATE)
    fetcher.export_to_csv()
