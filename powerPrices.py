# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:46:46 2021

@author: peter
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

"""
url = "https://www.nordpoolgroup.com/historical-market-data/"
absXpath = "/html/body/div[4]/div/div/div[2]/div/div/div[1]/div/table/tbody/tr[6]/td[1]/a"

driver = webdriver.Firefox(executable_path="C:\Program Files\Mozilla Firefox\geckodriver.exe")
driver.get(url)
driver.find_element_by_xpath(absXpath).click()

"""

url = "https://www.nordpoolgroup.com/globalassets/marketdata-excel-files/elspot-prices_2021_hourly_nok.xls"

r = requests.get(url, stream=True)
r2 = r.content.decode('utf-8')


with open("test.xls", "w") as f:
    #for chunk in r.iter_content(chunk_size=16*1024):
    print("Saving xls... ", end="")
    f.write(r2)
    print("Done")
        
df = pd.read_html("test.xls")[0]



df.to_csv("excel_to_csv.csv", index=False)