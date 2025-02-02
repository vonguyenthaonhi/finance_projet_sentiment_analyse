import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta


class HistoricalDataScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def _init_driver(self):
        """Initialise le navigateur avec les options requises."""
        options = Options()
        options.add_argument(
            "--start-maximized"
        )  # Démarrer le navigateur en plein écran
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def _accept_cookies(self):
        """Accepte les cookies si le bouton est disponible."""
        try:
            time.sleep(2)  # Attendre que la bannière des cookies apparaisse
            accept_cookies_button = self.driver.find_element(
                By.ID, "onetrust-accept-btn-handler"
            )
            accept_cookies_button.click()
            print("Cookies acceptés.")
            time.sleep(
                2
            )  # Attendre que la page se charge après avoir accepté les cookies
        except Exception as e:
            print(f"Erreur lors de l'acceptation des cookies : {e}")

    def scrape_data(self):
        """Scrape les données du site et les enregistre dans un fichier CSV."""
        try:
            self._init_driver()
            self.driver.get(self.url)
            self._accept_cookies()

            # Localiser le tableau contenant les données
            table_rows = self.driver.find_elements(
                By.XPATH, "//tr[contains(@class, 'historical-data-v2_price__atUfP')]"
            )
            if not table_rows:
                print("Aucune donnée trouvée dans le tableau.")
                return

            # Définir la plage de dates et le nom du fichier CSV
            today = datetime.today()
            last_month = today - timedelta(days=30)
            today_str = today.strftime("%Y-%m-%d")
            last_month_str = last_month.strftime("%Y-%m-%d")
            csv_file = f"Put_Call Ration EU - Données Historiques_{last_month_str}_to_{today_str}.csv"

            # Créer et remplir le fichier CSV
            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Date",
                        "Dernier",
                        "Ouverture",
                        "Haut",
                        "Bas",
                        "Volume",
                        "Variation (%)",
                    ]
                )

                for row in table_rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    if len(columns) >= 7:
                        date = columns[0].text.strip()
                        dernier = columns[1].text.strip()
                        ouverture = columns[2].text.strip()
                        haut = columns[3].text.strip()
                        bas = columns[4].text.strip()
                        volume = columns[5].text.strip()
                        variation = columns[6].text.strip()
                        writer.writerow(
                            [date, dernier, ouverture, haut, bas, volume, variation]
                        )

            print(f"Les données ont été enregistrées dans le fichier {csv_file}.")

        except Exception as e:
            print(f"Erreur lors de l'extraction des données : {e}")

        finally:
            if self.driver:
                self.driver.quit()
                print("Navigateur fermé.")


if __name__ == "__main__":
    scraper = HistoricalDataScraper(
        "https://fr.investing.com/indices/put-call-ratio-stoxx50-historical-data"
    )
    scraper.scrape_data()
