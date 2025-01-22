import csv
from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RatioScraper:
    """
    Classe pour scraper les ratios PUT/CALL depuis le site CBOE.
    """

    def __init__(self, start_date, end_date=None, csv_file="Put_Call Ratio US -Données Historiques.csv", verbose=False):
        """
        Initialise le scraper avec les paramètres requis.

        :param start_date: Date de début (datetime).
        :param end_date: Date de fin (datetime).
        :param csv_file: Chemin du fichier CSV où enregistrer les données.
        :param verbose: Affiche les étapes si True.
        """
        self.start_date = start_date
        self.end_date = end_date or datetime.today()
        self.csv_file = csv_file
        self.verbose = verbose
        self.driver = None
        self.cookies_accepted = False
        self.url_base = "https://www.cboe.com/us/options/market_statistics/daily/?dt="

    def _init_driver(self):
        """
        Initialise le driver Selenium.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)

    def _accept_cookies(self):
        """
        Accepte les cookies si nécessaire.
        """
        if not self.cookies_accepted:
            try:
                accept_button = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept"))
                )
                accept_button.click()
                if self.verbose:
                    print("Cookies acceptés.")
                self.cookies_accepted = True
            except Exception as e:
                if self.verbose:
                    print("Erreur lors de l'acceptation des cookies:", e)

    def _get_ratio_for_date(self, date_str):
        """
        Récupère les ratios pour une date donnée.

        :param date_str: Date sous format 'YYYY-MM-DD'.
        :return: Dictionnaire contenant les ratios (ou None si aucun).
        """
        try:
            url = f"{self.url_base}{date_str}"
            self.driver.get(url)
            time.sleep(2)  # Attendre que la page se charge

            # Accepter les cookies
            self._accept_cookies()

            # Sélectionner la ligne contenant le ratio PUT/CALL
            row = self.driver.find_element(
                By.CSS_SELECTOR,
                "#daily-market-statistics > div > div:nth-child(2) > table > tbody > tr:nth-child(1)"
            )
            columns = row.find_elements(By.TAG_NAME, "td")

            if len(columns) > 1:
                title = columns[0].text.strip()
                value = columns[1].text.strip()
                if "PUT/CALL RATIO" in title:
                    return {title: value}

            return None
        except Exception as e:
            if self.verbose:
                print(f"Erreur pour la date {date_str}: {e}")
            return None

    def _save_to_csv(self, data):
        """
        Sauvegarde les données dans un fichier CSV.

        :param data: Liste des données à sauvegarder.
        """
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Ratio Name", "Ratio Value"])  # En-têtes
            for row in data:
                writer.writerow(row)

    def scrape(self):
        """
        Lance le scraping des ratios PUT/CALL pour la plage de dates spécifiée.
        """
        self._init_driver()
        ratios_data = []

        current_date = self.start_date
        delta = timedelta(days=1)

        while current_date <= self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            if self.verbose:
                print(f"Récupération des données pour la date: {date_str}")

            ratios = self._get_ratio_for_date(date_str)
            if ratios:
                for name, value in ratios.items():
                    ratios_data.append([date_str, name, value])

            current_date += delta

        self._save_to_csv(ratios_data)
        self.driver.quit()
        if self.verbose:
            print(f"Données sauvegardées dans {self.csv_file}.")

    def __del__(self):
        """
        Détruit le driver Selenium à la fin.
        """
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    # Exemple d'utilisation
    scraper = RatioScraper(
        start_date=datetime(2024, 12, 31),
        end_date=datetime(2025, 1, 5),
        csv_file="Put_Call Ratio US -Données Historiques_12_2024_to_01_2025.csv",
        verbose=True,
    )
    scraper.scrape()
