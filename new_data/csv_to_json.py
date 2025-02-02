import csv
import json

def convertir_csv_en_json(fichier_csv, fichier_json):
    # Lire le fichier CSV
    with open(fichier_csv, mode='r', encoding='utf-8') as csv_file:
        lecteur_csv = csv.DictReader(csv_file)
        
        # Convertir en liste de dictionnaires
        donnees = list(lecteur_csv)
    
    # Écrire les données en JSON
    with open(fichier_json, mode='w', encoding='utf-8') as json_file:
        json.dump(donnees, json_file, indent=4, ensure_ascii=False)

# Remplacez par vos fichiers
fichier_csv = 'portfolio_weights.csv'
fichier_json = 'portfolio_weights.json'

convertir_csv_en_json(fichier_csv, fichier_json)
print(f"Le fichier JSON a été créé : {fichier_json}")
