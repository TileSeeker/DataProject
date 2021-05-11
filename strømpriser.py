"""
Created on Fri Mar 26 13:38:28 2021

@author: peter, sveien
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

class strømpris:
    def __init__(self, path):
        self.path = path
    
    def get(self):
        # Åner en autonom browser. SKal bare kjøres en gang
        # Må laste laste ned en selenum kompatibel driver
        driver = webdriver.Firefox(executable_path=self.path)
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
        
        strøm_pris = float(strøm[first_int_pos:last_int_pos])    
        driver.close()
        return strøm_pris


