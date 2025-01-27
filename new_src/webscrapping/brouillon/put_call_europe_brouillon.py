import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

# Initialiser le navigateur
options = Options()
options.add_argument("--start-maximized")  # Pour démarrer le navigateur en plein écran
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Ouvrir le site web
    driver.get("https://fr.investing.com/indices/put-call-ratio-stoxx50-historical-data")

    # Attendre que la page se charge et accepter les cookies
    time.sleep(2)  # Attendre que la bannière des cookies apparaisse
    accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    accept_cookies_button.click()

    # Attendre un moment pour que la page ajuste après avoir accepté les cookies
    time.sleep(2)

    # # Tentative de connexion
    # try:
    #     # Cliquer sur le bouton "Connexion"
    #     connexion_button = driver.find_element(By.XPATH, "//span[text()='Connexion']")
    #     connexion_button.click()

    #     # Attendre que la fenêtre de connexion apparaisse
    #     time.sleep(2)

    #     # Cliquer sur le bouton "Continuer avec Email"
    #     continue_with_email_button = driver.find_element(By.XPATH, "//span[text()='Continuer avec Email']")
    #     continue_with_email_button.click()

    #     # Attendre que les champs de saisie d'email et mot de passe apparaissent
    #     time.sleep(2)

    #     # Remplir le champ email
    #     email_field = driver.find_element(By.XPATH, "//input[@name='email']")
    #     email_field.send_keys("lucasvazelle@gmail.com")

    #     # Remplir le champ mot de passe
    #     password_field = driver.find_element(By.XPATH, "//input[@name='password']")
    #     password_field.send_keys("mdpMosef12@")

    #     # Cliquer sur le bouton "Connexion" pour se connecter
    #     login_button = driver.find_element(By.XPATH, "//button[@type='submit']//span[text()='Connexion']")
    #     login_button.click()

    #     # Attendre la fin du processus de connexion et le chargement de la page
    #     time.sleep(10)


    # except Exception as e:
    #     print(f"La connexion a échoué : {e}")
    #     # Cliquer sur le bouton "Fermer" si disponible
    #     try:
    #         close_button = driver.find_element(By.XPATH, "//svg[@viewBox='0 0 24 24' and contains(@class, 'w-4')]")
    #         close_button.click()
    #         print("Bouton 'Fermer' cliqué.")
    #     except Exception as close_error:
    #         print(f"Impossible de cliquer sur le bouton 'Fermer' : {close_error}")

    # Localiser le tableau contenant les données
    table_rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'historical-data-v2_price__atUfP')]")

    # Vérifier que des lignes sont trouvées
    if not table_rows:
        print("Aucune donnée trouvée dans le tableau.")
        driver.quit()
        exit(
    
    today = datetime.today()
    last_month = today - timedelta(days=30) 

    # Formater les dates au format souhaité (exemple: "2025-01-06" pour aujourd'hui)
    today_str = today.strftime("%Y-%m-%d")
    last_month_str = last_month.strftime("%Y-%m-%d")

    # Créer le nom du fichier CSV en incluant les dates
    csv_file = f"historical_data_{today_str}_{last_month_str}.csv"
    # Initialiser le fichier CSV
    # csv_file = "historical_data.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Écrire l'en-tête du fichier CSV
        writer.writerow(["Date", "Dernier", "Ouverture", "Haut", "Bas", "Volume", "Variation (%)"])

        # Parcourir les lignes du tableau et extraire les données
        for row in table_rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 7:  # Vérifier que la ligne contient au moins 7 colonnes
                date = columns[0].text.strip()
                dernier = columns[1].text.strip()
                ouverture = columns[2].text.strip()
                haut = columns[3].text.strip()
                bas = columns[4].text.strip()
                volume = columns[5].text.strip()
                variation = columns[6].text.strip()

                # Écrire les données dans le fichier CSV
                writer.writerow([date, dernier, ouverture, haut, bas, volume, variation])

    print(f"Les données ont été enregistrées dans le fichier {csv_file}.")

finally:
    # Fermer le navigateur
    driver.quit() 