# pobook to scrape
# penser à ajouter des try a notre script en cas d'erreur.
#lien utiles
#https://www.incrementors.com/blog/best-practices-for-robots-txt-seo/
#https://www.useragentlist.net/
# parseur 
import requests 
import pdb
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

# pdb.set_trace() #debeugeur python
reponse = requests.get(url)
reponse.encoding = reponse.apparent_encoding


def get_text_if_exist(e):
    if e:
        return e.text.strip()
    return None


if reponse.status_code == 200: 
#__________________________obligé____________________
    html = reponse.text
    f = open("reponse.html", 'w')
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, "lxml")
    test = soup.find("h1").text
    # la balise choisi grace à inspecter et cliquer sur le bonton qui fait le lien avec le site 
    print(test)
#_________________________________________importer 1 element__________
    #e_prix = soup.find("p", class_="price_color").text  #ajout class_="price_color car c'est une classe, ne pas faire attention au nom
    price = get_text_if_exist(soup.find("p", class_="price_color"))
    print(price)
#_________________________________________importer plusieurs element__________
    #tous les prix on la même balise
    # pas besoin de get_text_if_exist car utilse que pour un élément

    prices = soup.find_all("p", class_="price_color") 
    for price in prices: 
        print(price.text)

    titles = soup.find_all("a") 
    for title in titles: 
        if title.get("title"):
            print(title.get("title")) 
        
else:
    print("error", reponse.status_code)
print("succes")



# <p class="price_color">£47.82</p>
# <a href="catalogue/sharp-objects_997/index.html" 