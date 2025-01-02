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

us_put_cal_data ="https://www.cboe.com/us/options/market_statistics/daily/?_gl=1*eu24av*_up*MQ..*_ga*MTMxNjg2MjEuMTczNTc2MDExOQ..*_ga_5Q99WB9X71*MTczNTc2MDExOS4xLjEuMTczNTc2MDI2NC4wLjAuMA..&gclid=b2dc657e29da11fe0984020bb12ad73e&gclsrc=3p.ds&dt=2021-06-10