# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:38:28 2021

@author: peter
"""
# Må bruke Selenum for hente data
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
 

# Åner en autonom browser. SKal bare kjøres en gang
# Må laste laste ned en selenum kompatibel driver
driver = webdriver.Firefox(executable_path="C:\Program Files\Mozilla Firefox\geckodriver.exe")

# Nettside som skal scrapes
driver.get("https://www.trondelagkraft.no/strom/strompriser/")
 
content = driver.page_source
soup = BeautifulSoup(content, features="lxml")
strøm = str(soup.find("h2", attrs={"class":"pt-xxxs pb-xs"}))
strøm = strøm.replace(',', '.')

first_int_pos = 0    
for i in range(65, len(strøm)):

    try: 
        int(strøm[i])
        first_int_pos = i
        break
    
    except:
        pass

last_int_pos = 0    
for i in range(len(strøm)-3, first_int_pos , -1):
    
    try: 
        int(strøm[i])
        last_int_pos = i
        break
    
    except:
        pass    
    
strøm_pris = (strøm[first_int_pos:last_int_pos])    

    

print(first_int_pos)
print(last_int_pos)
print(strøm_pris)
print(strøm)
driver.close()