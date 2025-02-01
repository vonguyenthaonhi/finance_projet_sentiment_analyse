import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2, norm

# --- PARAMÈTRES ---
DATA_FOLDER = "../new_data/full_data"
OUTPUT_FOLDER = "../new_output/results/var"
GRAPH_FOLDER = os.path.join(OUTPUT_FOLDER, "graphs")
WINDOW = 252  # Fenêtre de 1 an
TAIL = 0.05  # 5% quantile pour la VaR

# Création des dossiers de sortie si inexistants
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# Fonction pour le calcul de la VaR historique et ajustée (pcr)

def hist_var(serie, window, tail):
    """Calcul de la VaR historique avec bootstrap."""
    n = len(serie)
    VaR = np.zeros(n)

    for i in range(window, n):
        z = serie[i-window:i]
        sample = np.random.choice(z, size=100000, replace=True)
        sample.sort()
        VaR[i] = sample[int(np.ceil(len(sample) * tail)) - 1]

    return VaR


def adjust_var(VaR_hist, put_call_ratio, neutral_value=1.0, bearish_threshold=1.2, bullish_threshold=0.8):
    VaR_adjusted = VaR_hist.copy()

    for i in range(len(VaR_hist)):
        pcr = put_call_ratio[i]  # Récupérer le ratio pour l'index i

        if pcr < bullish_threshold:  # Bullish sentiment
            adjustment = 1 - 0.1 * abs(pcr - neutral_value)
            VaR_adjusted.iloc[i] *= max(0.8, adjustment)  # Appliquer l'ajustement à la i-ème ligne
        elif pcr > bearish_threshold:  # Bearish sentiment
            adjustment = 1 + 0.1 * abs(pcr - neutral_value)
            VaR_adjusted.iloc[i] *= min(1.2, adjustment)  # Appliquer l'ajustement à la i-ème ligne

    return VaR_adjusted



# Fonctions pour le Backtesting

def kupiec_test(returns, var, alpha=0.05):
    """Test de Kupiec pour valider la VaR."""
    violations = returns < var
    T, N = len(returns), violations.sum()
    m = T - N
    tho = N / T if T > 0 else 0

    if N == 0 or T == 0 or tho == 0:
        return {"Total Observations": T, "Violations": N, "Kupiec Statistic": np.nan, "P-Value": np.nan}

    kupiec_stat = -2 * np.log(((1 - alpha)**m * alpha**N) / ((1 - tho)**m * tho**N))
    p_value = 1 - chi2.cdf(kupiec_stat, df=1)

    return {"Total Observations": T, "Violations": N, "Kupiec Statistic": round(kupiec_stat, 4), "P-Value": round(p_value, 4)}


def binomial_test(returns, var, alpha=0.05):
    """Test binomial pour valider la VaR."""
    violations = returns < var
    T, N = len(returns), violations.sum()

    if T == 0 or T * alpha * (1 - alpha) == 0:
        return {"Total Observations": T, "Violations": N, "Binomial Statistic": np.nan, "P-Value": np.nan}

    binomial_stat = (N - (T * alpha)) / np.sqrt(T * alpha * (1 - alpha))
    p_value = 2 * (1 - norm.cdf(abs(binomial_stat)))

    return {"Total Observations": T, "Violations": N, "Binomial Statistic": round(binomial_stat, 4), "P-Value": round(p_value, 4)}


# --- TRAITEMENT DES DONNÉES ---
files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]
results = []

for file in files:
    df = pd.read_csv(os.path.join(DATA_FOLDER, file))
    df['Date'] = pd.to_datetime(df['Date'])

    # Extraction des colonnes nécessaires
    serie, put_call_ratio = df['Daily Return'].values, df['Put-Call Ratio'].values

    # Calcul de la VaR
    df['VaR_Hist'] = hist_var(serie, WINDOW, TAIL)
    df['VaR_Adjusted'] = adjust_var(df['VaR_Hist'], put_call_ratio)

    asset_name = file.split('_')[0]
    df['Asset'] = asset_name
    results.append(df)

# Fusion des résultats et exportation
final_df = pd.concat(results, ignore_index=True)
final_file = os.path.join(OUTPUT_FOLDER, "financial_data_with_var.csv")
final_df.to_csv(final_file, index=False)
print(f"✅ Données enregistrées dans {final_file}")



# --- CRÉATION DES GRAPHIQUES ---
assets = final_df['Asset'].unique()
for asset in assets:
    asset_data = final_df[final_df['Asset'] == asset]
    
    # Filtrage des données pour ne conserver que celles à partir de 2020-10-15
    asset_data = asset_data[asset_data['Date'] >= '2020-10-15']

    plt.figure(figsize=(12, 6))
    plt.plot(asset_data['Date'], asset_data['Daily Return'], label='Rendement', color='black', linewidth=0.8)
    plt.plot(asset_data['Date'], asset_data['VaR_Hist'], label='VaR Historique', color='blue', linewidth=2)
    plt.plot(asset_data['Date'], asset_data['VaR_Adjusted'], label='VaR Ajustée', color='red', linewidth=1)
    plt.title(f"Value at Risk pour {asset}", fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Valeurs', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(alpha=0.5)
    plt.tight_layout()

    graph_path = os.path.join(GRAPH_FOLDER, f"{asset}_VaR.png")
    plt.savefig(graph_path)
    plt.close()
    print(f"📊 Graphique sauvegardé : {graph_path}")


# --- VALIDATION AVEC TESTS DE KUPIEC ET BINOMIAL ---
kupiec_results, binomial_results = [], []
for asset in assets:
    asset_data = final_df[final_df['Asset'] == asset]
    
    # Filtrage des données pour ne conserver que celles à partir de 2020-10-15
    asset_data = asset_data[asset_data['Date'] >= '2020-10-15']
    
    returns, var_hist, var_adj = asset_data['Daily Return'], asset_data['VaR_Hist'], asset_data['VaR_Adjusted']

    for var_type, var in [("VaR_Hist", var_hist), ("VaR_Adjusted", var_adj)]:
        kupiec_res = kupiec_test(returns, var)
        binomial_res = binomial_test(returns, var)

        kupiec_res.update({"Asset": asset, "VaR Type": var_type})
        binomial_res.update({"Asset": asset, "VaR Type": var_type})

        kupiec_results.append(kupiec_res)
        binomial_results.append(binomial_res)

# Sauvegarde des résultats des tests
pd.DataFrame(kupiec_results).to_csv(os.path.join(OUTPUT_FOLDER, "kupiec_test_results.csv"), index=False)
pd.DataFrame(binomial_results).to_csv(os.path.join(OUTPUT_FOLDER, "binomial_test_results.csv"), index=False)
print("✅ Résultats des tests sauvegardés !")


# Sauvegarde des résultats des tests
pd.DataFrame(kupiec_results).to_csv(os.path.join(OUTPUT_FOLDER, "kupiec_test_results.csv"), index=False)
pd.DataFrame(binomial_results).to_csv(os.path.join(OUTPUT_FOLDER, "binomial_test_results.csv"), index=False)
print("✅ Résultats des tests sauvegardés !")
