# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 08:03:47 2021

@author: nurarif.zanuri
"""

#download from chrome in a specific folder.
#read metadata and delete.

from selenium import webdriver
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def edge_setup():

  driver = webdriver.Edge(executable_path=r"D:\ESDA\Crawling_Compilation\msedgedriver.exe")
  return driver

def convert_html_bs(a):
  elementHTML = a.get_attribute('outerHTML') #gives exact HTML content of the elemen    t
  elementSoup = BeautifulSoup(elementHTML,'html.parser')
  
  return elementSoup
def go_to_next_page(driver):
    try:
      next_page = driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
      next_page.click()
      return 1
    except Exception as e:
      print("ERROR:{}".format(e))
      return 0
def get_info(driver,url_list,title_list,a_list,a):
    html_bs = convert_html_bs(driver.find_element_by_tag_name("body"))
    result_list = html_bs.find_all("div",{"class":"yuRUbf"})
    for r in result_list:
      url_list.append(r.find("a", href = True)['href'])
      title_list.append(r.find("h3",{"class":"LC20lb MBeuO DKV0Md"}).text)
      a_list.append(a)
    return url_list, title_list,a_list
def main():
  driver = edge_setup()
  area = ["'sabah'","'sarawak'","'peninsular+malaysia'","'semenanjung+malaysia'","'malay+basin'","'penyu+basin'"]
  url_list = []
  title_list = []
  a_list = []
  for a in area:
      url = "https://www.google.com/search?q=filetype%3Apdf+engineering+geology+"+a
      cont = 1
      driver.get(url)
      now = datetime.now()
      while cont == 1:
        url_list, title_list,a_list = get_info(driver,url_list, title_list,a_list,a)
        cont = go_to_next_page(driver)
  print("HABIS")
  pd.DataFrame({"URL":url_list,"TITLE":title_list,"DATE":[now.strftime("%m/%d/%Y, %H:%M:%S")]*len(url_list),"Region":a_list}).to_excel(r"Scraped_1.xlsx")

if __name__ == "__main__":
    main()
