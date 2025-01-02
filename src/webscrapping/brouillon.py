from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup


# URL de la page contenant les ratios
html = """https://www.cboe.com/us/options/market_statistics/daily/?_gl=1*eu24av*_up*MQ..*_ga*MTMxNjg2MjEuMTczNTc2MDExOQ..*_ga_5Q99WB9X71*MTczNTc2MDExOS4xLjEuMTczNTc2MDI2NC4wLjAuMA..&gclid=b2dc657e29da11fe0984020bb12ad73e&gclsrc=3p.ds&dt=2021-06-10"""

soup = BeautifulSoup(html, "html.parser")

# Trouver toutes les lignes de la table contenant des ratios
table_rows = soup.find_all("tr")

# Dictionnaire pour stocker les ratios
ratios = {}

# Boucler à travers chaque ligne pour récupérer le ratio
for row in table_rows:
    cells = row.find_all("td")
    if len(cells) == 2:  # Si la ligne a deux cellules, le ratio est dans la seconde
        ratio_name = cells[0].text.strip()
        ratio_value = cells[1].text.strip()
        ratios[ratio_name] = ratio_value

# Afficher les résultats
for ratio_name, ratio_value in ratios.items():
    print(f"{ratio_name}: {ratio_value}")
