import yfinance as yf
import pandas as pd

# Liste des symboles boursiers des entreprises
symbols = {
    "Total Energies": "TTE.PA",  # Symbole de Total Energies sur Euronext Paris
    "FMC Corp": "FMC",
    "BP PLC": "BP",
    "Stora Enso": "STE",  # Symbole de Stora Enso
    "BHP Group": "BHP"
}

# Fonction pour récupérer les rendements journaliers et la volatilité journalière
def get_financial_data(symbol, start_date, end_date):
    try:
        # Télécharger les données financières pour la période spécifiée
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            return None  # Si aucune donnée n'est disponible

        # Vérification de la présence de NaN dans les données de "Close"
        if data['Close'].isnull().any():
            print(f"Des valeurs manquantes trouvées dans 'Close' pour {symbol}")

        # Calculer les rendements journaliers (en pourcentage)
        data['Daily Return'] = data['Close'].pct_change() * 100
        # Vérifier si le rendement est NaN et, si c'est le cas, forcer à 0 pour le premier jour
        if pd.isna(data['Daily Return'].iloc[0]):
            data['Daily Return'].iloc[0] = 0.0

        # Calculer la volatilité journalière (écart-type des rendements)
        volatility = data['Daily Return'].std() * (252 ** 0.5)  # Annualisé

        # Retourner les données avec les rendements journaliers
        return data[['Close', 'Daily Return']], volatility

    except Exception as e:
        print(f"Erreur avec {symbol}: {e}")
        return None

start_date = "2019-01-01"
end_date = "2024-12-31"

# Pour chaque entreprise, obtenir les données journalières et exporter un fichier CSV
for company, symbol in symbols.items():
    data, volatility = get_financial_data(symbol, start_date, end_date)
    if data is not None:
        # Ajouter la colonne de volatilité pour chaque ligne
        data['Volatility (%)'] = volatility
        
        # Formater la colonne "Date" pour ne garder que la date sans heure et fuseau horaire
        data.index = data.index.strftime('%Y-%m-%d')

        # Exporter les données dans un fichier CSV pour chaque entreprise
        file_name = f"new_data/volatility/{company.replace(' ', '_')}_financial_data_23k.csv"
        data.to_csv(file_name, index=True)
        print(f"Fichier CSV généré pour {company} : {file_name}")
    else:
        print(f"Aucune donnée disponible pour {company}.")
