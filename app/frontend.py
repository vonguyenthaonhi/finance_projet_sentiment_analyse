import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# URL de l'API FastAPI
API_URL = "http://localhost:8000/api/v1/put-call-ratio-us"

# Titre de l'application Streamlit
st.title("Put-Call Ratio US")

# Description
st.write("""
Cette application vous permet de récupérer les données du Put-Call Ratio pour une date donnée ou pour l'ensemble des dates disponibles.
Entrez une date pour obtenir les informations correspondantes ou visualisez l'évolution des ratios pour toutes les dates.
""")

# Entrée de la date par l'utilisateur
date_input = st.text_input("Entrez la date (YYYY-MM-DD):", value="2024-01-01")

# Bouton pour récupérer les données pour une date spécifique
if st.button("Obtenir les données pour cette date"):
    try:
        # Vérification du format de la date
        datetime.strptime(date_input, "%Y-%m-%d")
        
        # Envoi de la requête GET à l'API FastAPI pour la date spécifique
        response = requests.get(f"{API_URL}/{date_input}")
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"Date: {data['date']}")
            st.write(f"Nom du ratio: {data['ratio_name']}")
            st.write(f"Valeur du ratio: {data['ratio_value']}")
        elif response.status_code == 404:
            st.error(f"Aucune donnée trouvée pour la date {date_input}. Rappel, les données ne sont pas disponibles les week-ends.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
    except ValueError:
        st.error("Format de date invalide. Utilisez 'YYYY-MM-DD'.")

# Bouton pour récupérer toutes les données
if st.button("Voir l'évolution des ratios"):
    # Envoi de la requête GET pour récupérer toutes les données
    response_all = requests.get(f"{API_URL}/")
    
    if response_all.status_code == 200:
        data_all = response_all.json()
        
        # Convertir les données en DataFrame pour faciliter l'affichage et la visualisation
        df = pd.DataFrame(data_all)
        df['date'] = pd.to_datetime(df['date'])
        df['ratio_value'] = pd.to_numeric(df['ratio_value'], errors='coerce')

        # Affichage des données sous forme de tableau
        st.write(df)

        # Affichage du graphique
        st.subheader("Évolution du Put-Call Ratio")
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['ratio_value'], marker='o', linestyle='-', color='b')
        plt.title("Put-Call Ratio US au fil du temps")
        plt.xlabel("Date")
        plt.ylabel("Put-Call Ratio")
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.error(f"Erreur lors de la récupération des données : {response_all.status_code} - {response_all.text}")
