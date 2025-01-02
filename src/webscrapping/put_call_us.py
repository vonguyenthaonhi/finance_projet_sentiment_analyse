import csv
from datetime import date, datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# URL de base
url_base = """https://www.cboe.com/us/options/market_statistics/daily/"""

# Initialisation du driver Selenium
driver = webdriver.Chrome()

# Variable pour vérifier si les cookies ont été acceptés
cookies_accepted = False

# Fonction pour accepter les cookies
def accept_cookies():
    global cookies_accepted
    try:
        # Si les cookies n'ont pas encore été acceptés, les accepter
        if not cookies_accepted:
            accept_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept"))
            )
            accept_button.click()
            print("Cookies acceptés.")
            cookies_accepted = True  # Marquer comme accepté pour ne plus le refaire
    except Exception as e:
        print("Erreur lors de l'acceptation des cookies:", e)

    
# Fonction pour récupérer le ratio d'une date donnée
def get_ratio_for_date(date_str):
    try:
        # Construire l'URL en fonction de la date
        url = f"""{url_base}?_gl=1*eu24av*_up*MQ..*_ga*MTMxNjg2MjEuMTczNTc2MDExOQ..*_ga_5Q99WB9X71*MTczNTc2MDExOS4xLjEuMTczNTc2MDI2NC4wLjAuMA..&gclid=b2dc657e29da11fe0984020bb12ad73e&gclsrc=3p.ds&dt={date_str}"""
        
        # Accéder à l'URL
        driver.get(url)
        time.sleep(2)  # Attendre que la page se charge
        
        # Appeler la fonction pour accepter les cookies (seulement une fois)
        accept_cookies()

        # Trouver la ligne spécifique dans le tableau via CSS Selector
        row = driver.find_element(By.CSS_SELECTOR, "#daily-market-statistics > div > div:nth-child(2) > table > tbody > tr:nth-child(1)")
        
        # Extraire les colonnes de la ligne
        columns = row.find_elements(By.TAG_NAME, "td")
        
        if len(columns) > 1:
            title = columns[0].text.strip()
            value = columns[1].text.strip()
            
            # Vérifier si le titre correspond à un ratio
            if "PUT/CALL RATIO" in title:
                return {title: value}
        
        return None
    
    except Exception as e:
        print(f"Erreur pour la date {date_str}: {e}")
        return None




# Fonction pour enregistrer les données dans un fichier CSV
def save_to_csv(data):
    with open("ratios.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Ratio Name", "Ratio Value"])  # En-têtes du fichier CSV
        for row in data:
            writer.writerow(row)

# Itérer sur les dates à partir du 10/05/2019
start_date = datetime(2024, 12, 7)
end_date = datetime.today()
delta = timedelta(days=1)

# Liste pour stocker les résultats
ratios_data = []

# Itérer sur les dates
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")  # Formater la date en YYYY-MM-DD
    print(f"Récupération des données pour la date: {date_str}")
    
    # Récupérer les ratios pour cette date
    ratios = get_ratio_for_date(date_str)
    
    if ratios:
        # Ajouter chaque ratio trouvé avec son nom et valeur
        for name, value in ratios.items():
            ratios_data.append([date_str, name, value])
    
    current_date += delta  # Passer au jour suivant

# Sauvegarder les données dans le fichier CSV
save_to_csv(ratios_data)

# Fermer le navigateur
driver.quit()
