import yfinance as yf
import os

# Ticker de l'ETF
ticker_EU = "OBLI.PA"  # Amundi PEA Obligations d'État Euro UCITS ETF
ticker_US = "^IRX" 

# Période souhaitée
start_date = "2023-01-01"
end_date = "2023-12-31"

# Téléchargement des données
rfr_eu_data = yf.download(ticker_EU, start=start_date, end=end_date, interval="1d")
rfr_us_data = yf.download(ticker_US, start=start_date, end=end_date, interval="1d")

#Nettoyage
rfr_eu_data.reset_index(inplace=True)
rfr_us_data.reset_index(inplace=True)

rfr_eu_data.columns = rfr_eu_data.columns.get_level_values(0)
rfr_us_data.columns = rfr_us_data.columns.get_level_values(0)

# Chemin du dossier de destination
output_directory = "new_data/volatility"
output_file_path_eu = os.path.join(output_directory, "risk_free_rate_EU.csv")
output_file_path_us = os.path.join(output_directory, "risk_free_rate_US.csv")

# Sauvegarde des données dans un fichier CSV
rfr_eu_data.to_csv(output_file_path_eu)
rfr_us_data.to_csv(output_file_path_us)

