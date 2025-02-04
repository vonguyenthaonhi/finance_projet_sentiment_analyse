import csv
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RatioScraperUS:
    """
    Scraper des ratios PUT/CALL sur le site CBOE.
    """

    def __init__(
        self,
        start_date: str,
        end_date: str = None,
        csv_file: str = "put_call_ratios.csv",
        verbose: bool = False,
    ):
        """
        Initialise les paramètres du scraping.

        :param start_date: Date de début (format YYYY-MM-DD).
        :param end_date: Date de fin (optionnelle, par défaut aujourd’hui).
        :param csv_file: Nom du fichier CSV pour sauvegarder les résultats.
        :param verbose: Affiche les logs si True.
        """
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = (
            datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.today()
        )
        self.csv_file = csv_file
        self.verbose = verbose
        self.driver = None
        self.url_base = "https://www.cboe.com/us/options/market_statistics/daily/?dt="
        self.cookies_accepted = False

    def _init_driver(self):
        """Initialise le driver Selenium."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Mode sans interface graphique
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--remote-debugging-port=9222")
	self.driver = webdriver.Chrome(options=options)

    def _accept_cookies(self):
        """Accepte les cookies si présents."""
        if not self.cookies_accepted:
            try:
                accept_button = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept"))
                )
                accept_button.click()
                if self.verbose:
                    print("✅ Cookies acceptés.")
                self.cookies_accepted = True
            except Exception:
                if self.verbose:
                    print("⚠️ Aucun cookie à accepter.")

    def _get_ratio_for_date(self, date_str: str):
        """
        Récupère le ratio PUT/CALL pour une date donnée.

        :param date_str: Date sous format 'YYYY-MM-DD'.
        :return: Dictionnaire avec la date, le nom du ratio et la valeur.
        """
        try:
            url = f"{self.url_base}{date_str}"
            self.driver.get(url)
            time.sleep(2)  # Pause pour éviter les problèmes de chargement

            self._accept_cookies()

            # Récupérer la ligne contenant le ratio PUT/CALL
            row = self.driver.find_element(
                By.CSS_SELECTOR,
                "#daily-market-statistics > div > div:nth-child(2) > table > tbody > tr:nth-child(1)",
            )
            columns = row.find_elements(By.TAG_NAME, "td")

            if len(columns) > 1:
                title = columns[0].text.strip()
                value = columns[1].text.strip()
                if "PUT/CALL RATIO" in title:
                    return {"date": date_str, "ratio_name": title, "ratio_value": value}

        except Exception as e:
            if self.verbose:
                print(f"⚠️ Erreur pour {date_str}: {e}")

        return None

    def scrape_ratios(self):
        """
        Lance le scraping sur la plage de dates définie.

        :return: Liste des résultats sous forme de dictionnaires.
        """
        self._init_driver()
        ratios_data = []

        current_date = self.start_date
        delta = timedelta(days=1)

        while current_date <= self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            if self.verbose:
                print(f"🔎 Scraping pour la date: {date_str}")

            ratio = self._get_ratio_for_date(date_str)
            if ratio:
                ratios_data.append(ratio)

            current_date += delta

        self.driver.quit()
        return ratios_data

    def save_to_csv(self, data):
        """
        Sauvegarde les résultats du scraping dans un fichier CSV.

        :param data: Liste des données à enregistrer.
        """
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Ratio Name", "Ratio Value"])
            for row in data:
                writer.writerow([row["date"], row["ratio_name"], row["ratio_value"]])

        if self.verbose:
            print(f"✅ Données sauvegardées dans {self.csv_file}.")
