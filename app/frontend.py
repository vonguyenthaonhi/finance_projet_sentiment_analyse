import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# URL de base de l'API FastAPI
API_URL = "http://localhost:8000/api/v1"

# Titre principal
st.title("Put-Call Ratio et portefeuille")

st.write("""
Bienvenue dans cette application permettant d'interagir avec l'API pour récupérer et analyser les ratios PUT/CALL.
Vous pouvez soit afficher les données historiques, soit lancer un scraping pour récupérer de nouvelles données.
         Vouvez aussi calculer des poids de pondération d'actif pour la construction de portefeuille basé sur le secteur de l'énergie et les ratios put/call.

""")

st.title("Put-Call Ratio US et Europe")


# __________________________LANCER UN SCRAPING US-______________________
st.header(" 📊 Scraping des Ratios PUT/CAL US")
st.write("Cliquez sur le bouton ci-dessous")

# Formulaire pour entrer les paramètres du scraping
with st.form("scraping_form"):
    start_date = st.text_input("📅 Date de début (YYYY-MM-DD) :", value="2025-01-01")
    end_date = st.text_input("📅 Date de fin (YYYY-MM-DD, optionnel) :", value="2025-01-05")
    save = st.checkbox("💾 Sauvegarder en CSV")

    submit_scraping = st.form_submit_button("🚀Lancer le Scraping")

if submit_scraping:
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        end_date_param = f"&end_date={end_date}" if end_date else ""

        response_scrape = requests.get(f"{API_URL}/scrape-put-call-ratio_us/?start_date={start_date}{end_date_param}&save={save}")

        if response_scrape.status_code == 200:
            result = response_scrape.json()
            st.success("✅ Scraping terminé avec succès !")
            st.json(result)  # Afficher les données récupérées
        else:
            st.error(f"❌ Erreur : {response_scrape.status_code} - {response_scrape.text}")
    except ValueError:
        st.error("❌ Format de date invalide. Utilisez 'YYYY-MM-DD'.")

# ______________________SECTION 2 : LANCER UN SCRAPING PUT CALL Europe______________

st.header("📊 Scraper Put-Call Ratio Europe")

st.write("Cliquez sur le bouton ci-dessous pour lancer le scraping.")

if st.button("🚀 Lancer le Scraping"):
    response = requests.get(f"{API_URL}/scrape-put-call-ratio-eu/")
    
    if response.status_code == 200:
        data = response.json()
        st.success("✅ Scraping terminé avec succès !")

        if "data" in data and data["data"]:
            df = pd.DataFrame(data["data"])
            df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
            df["Dernier"] = df["Dernier"].str.replace(",", ".").astype(float)

            st.write("📋 **Données récupérées :**")
            st.dataframe(df)

            st.subheader("📈 Graphique du Put-Call Ratio")
            st.line_chart(df.set_index("Date")["Dernier"])
        else:
            st.warning("⚠️ Aucune donnée récupérée.")
    else:
        st.error(f"❌ Erreur : {response.status_code} - {response.text}")









#__________________________Graph historique__________________________


st.header("📈 Évolution du Put-Call Ratio US")
st.write("Cliquez sur le bouton ci-dessous")

if st.button("Charger toutes les données et afficher le graphique"):
    response_all = requests.get(f"{API_URL}/put-call-ratio-us/")
    
    if response_all.status_code == 200:
        data_all = response_all.json()
        df = pd.DataFrame(data_all)
        df['date'] = pd.to_datetime(df['date'])
        df['ratio_value'] = pd.to_numeric(df['ratio_value'], errors='coerce')

        st.write("📋 **Données disponibles :**")
        st.dataframe(df)

        st.subheader("📊 Graphique du Put-Call Ratio")
        st.line_chart(df.set_index("date")["ratio_value"])

    else:
        st.error(f"❌ Erreur lors de la récupération des données : {response_all.status_code} - {response_all.text}")




#__________________________Graph historique__________________________

st.header("📈 Évolution du Put-Call Ratio Europe")

st.write("Cliquez sur le bouton ci-dessous ")

if st.button("Charger toutes les données  et afficher le graphique"):
    response = requests.get(f"{API_URL}/put-call-ratio-eu/")

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Données chargées avec succès !")

        if data:
            df = pd.DataFrame(data)
            
            # Convertir les valeurs numériques et les dates
            df["Date"] = pd.to_datetime(df["﻿\"Date\""], format="%d/%m/%Y", dayfirst=True)
            df["Dernier"] = df["Dernier"].str.replace(",", ".").astype(float)

            st.write("📋 **Données récupérées :**")
            st.dataframe(df)

            st.subheader("📈 Graphique du Put-Call Ratio")
            st.line_chart(df.set_index("Date")["Dernier"])
        else:
            st.warning("⚠️ Aucune donnée trouvée.")
    else:
        st.error(f"❌ Erreur : {response.status_code} - {response.text}")


st.title("Portefeuille basé sur des actifs du secteur de l'énergie")



#_____________________________Var_____________________


st.header("📊 Value at risk du portefeuille")

st.write("Cliquez sur le bouton ci-dessous")

if st.button("🔄 Charger les données VaR"):
    response = requests.get(f"{API_URL}/var-data/")

    if response.status_code == 200:
        data = response.json()
        st.success("✅ Données chargées avec succès !")

        if data:
            df = pd.DataFrame(data)
            
            # Convertir les valeurs numériques et les dates
            df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
            df["Close"] = df["Close"].astype(float)
            df["Daily Return"] = df["Daily Return"].astype(float)
            df["Put-Call Ratio"] = df["Put-Call Ratio"].astype(float)
            df["VaR_Hist"] = df["VaR_Hist"].astype(float)
            df["VaR_Adjusted"] = df["VaR_Adjusted"].astype(float)
            st.write("📋 **Données récupérées :**")
            st.dataframe(df)

            st.subheader("📈 Graphique VaR et rendement des actifs")  
            # st.line_chart(df.set_index("Date")[["Daily Return", "VaR_Hist", "VaR_Adjusted"]])

    
        else:
            st.warning("⚠️ Aucune donnée trouvée.")
    else:
        st.error(f"❌ Erreur : {response.status_code} - {response.text}")

if "var_data" not in st.session_state:
    st.session_state.var_data = None

if st.button("📈 Afficher les données VaR du portefeuille"):
    response = requests.get(f"{API_URL}/var-data/")
    if response.status_code == 200:
        st.session_state.var_data = response.json()  # Stocker les données en session
        st.success("✅ Données chargées avec succès !")
    else:
        st.error(f"❌ Erreur : {response.status_code} - {response.text}")

if st.session_state.var_data:
    df = pd.DataFrame(st.session_state.var_data)

    # Convertir les valeurs numériques et les dates
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Close"] = df["Close"].astype(float)
    df["Daily Return"] = df["Daily Return"].astype(float)
    df["Put-Call Ratio"] = df["Put-Call Ratio"].astype(float)
    df["VaR_Hist"] = df["VaR_Hist"].astype(float)
    df["VaR_Adjusted"] = df["VaR_Adjusted"].astype(float)

    # Sélecteur d'entreprise
    entreprises = df["Asset"].unique()
    choix_entreprise = st.selectbox("Choisissez une entreprise :", entreprises)

    # Filtrer les données en fonction de l'entreprise sélectionnée
    df_selection = df[df["Asset"] == choix_entreprise]

    # Afficher le graphique
    st.line_chart(df_selection.set_index("Date")[["Daily Return", "VaR_Hist", "VaR_Adjusted"]])






#_____________________________Poids du portefeuille_____________________
st.header("Calcul des poids du portefeuille")
st.write("Choissisez vos seuil d'achat/ vente en fonction de la valeur du put call ratio du marché des actifs")

# Seuils pour les signaux
bullish_threshold = st.number_input("Seuil Bullish", value=-1.0)
bearish_threshold = st.number_input("Seuil Bearish", value=1.0)

if st.button(" 🚀Calculer les Poids"):
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/calculate_weights/",
        params={"bullish_threshold": bullish_threshold, "bearish_threshold": bearish_threshold},
    )

    if response.status_code == 200:
        weights_data = response.json()["weights"]
        weights_df = pd.DataFrame(weights_data)

        st.write("### Poids du Portefeuille")
        st.dataframe(weights_df)
    else:
        st.error("Erreur lors du calcul des poids.")



