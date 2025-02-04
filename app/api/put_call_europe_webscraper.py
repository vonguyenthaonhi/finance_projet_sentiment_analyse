import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta


class LastMonthDataScraperEurope:
    def __init__(
        self,
        url="https://fr.investing.com/indices/put-call-ratio-stoxx50-historical-data",
    ):
        self.url = url
        self.driver = None
        self.data = []  # Stocker les données en mémoire

    def _init_driver(self):
        """Initialise le navigateur avec les options requises."""
        options = Options()
        options.add_argument("--headless")  # Exécuter en mode headless (sans fenêtre)
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-gpu")
        options.add_argument("--user-data-dir=/tmp")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def _accept_cookies(self):
        """Accepte les cookies si le bouton est disponible."""
        try:
            time.sleep(2)
            accept_cookies_button = self.driver.find_element(
                By.ID, "onetrust-accept-btn-handler"
            )
            accept_cookies_button.click()
            time.sleep(2)
        except Exception:
            pass

    def scrape_data(self):
        """Scrape les données et les retourne sous forme de liste de dictionnaires."""
        try:
            self._init_driver()
            self.driver.get(self.url)
            self._accept_cookies()

            table_rows = self.driver.find_elements(
                By.XPATH, "//tr[contains(@class, 'historical-data-v2_price__atUfP')]"
            )
            if not table_rows:
                return []

            self.data = []
            for row in table_rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 7:
                    self.data.append(
                        {
                            "Date": columns[0].text.strip(),
                            "Dernier": columns[1].text.strip(),
                            "Ouverture": columns[2].text.strip(),
                            "Haut": columns[3].text.strip(),
                            "Bas": columns[4].text.strip(),
                            "Volume": columns[5].text.strip(),
                            "Variation (%)": columns[6].text.strip(),
                        }
                    )

            return self.data

        except Exception as e:
            print(f"Erreur de scraping : {e}")
            return []

        finally:
            if self.driver:
                self.driver.quit()

    def save_to_csv(self):
        """Enregistre les données dans un fichier CSV."""
        if not self.data:
            return None

        today = datetime.today()
        last_month = today - timedelta(days=30)
        filename = f"Put_Call_Ratio_EU_{last_month.strftime('%Y-%m-%d')}_to_{today.strftime('%Y-%m-%d')}.csv"

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)

        return filename
