import csv
from datetime import date, datetime
import os
import random
import urllib
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Initialiser le navigateur
options = Options()
options.add_argument("--start-maximized")  # Pour démarrer le navigateur en plein écran
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ouvrir le site web
driver.get("https://fr.investing.com/indices/put-call-ratio-stoxx50-historical-data")

# Attendre que la page se charge et accepter les cookies
time.sleep(2)  # Attendre que la bannière des cookies apparaisse
accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookies_button.click()

# Attendre un moment pour que la page ajuste après avoir accepté les cookies
time.sleep(2)

# Cliquer sur le bouton "Connexion"
connexion_button = driver.find_element(By.XPATH, "//span[text()='Connexion']")
connexion_button.click()

# Attendre que la fenêtre de connexion apparaisse
time.sleep(2)

# Cliquer sur le bouton "Continuer avec Email"
continue_with_email_button = driver.find_element(By.XPATH, "//span[text()='Continuer avec Email']")
continue_with_email_button.click()

# Attendre que les champs de saisie d'email et mot de passe apparaissent
time.sleep(2)

# Remplir le champ email
email_field = driver.find_element(By.XPATH, "//input[@name='email']")
email_field.send_keys("lucasvazelle@gmail.com")

# Remplir le champ mot de passe
password_field = driver.find_element(By.XPATH, "//input[@name='password']")
password_field.send_keys("mdpMosef12@")

# Cliquer sur le bouton "Connexion" pour se connecter
login_button = driver.find_element(By.XPATH, "//button[@type='submit']//span[text()='Connexion']")
login_button.click()

# Attendre la fin du processus de connexion et le chargement de la page
time.sleep(20)

# Cliquer sur le bouton "Télécharger" pour lancer le téléchargement des données
download_button = driver.find_element(By.XPATH, "//span[text()='Télécharger']")
download_button.click()

# Attendre que le téléchargement soit lancé (ajuster en fonction de la vitesse de connexion)
time.sleep(5)

# Fermer le navigateur
driver.quit()
