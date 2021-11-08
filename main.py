import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests

startURL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("/chromedriver")
headers = ["STAR","DISTANCE","MASS","RADIUS"]
planetDataTemp = []
planetDataSpecific = []
planetData = []

# To delay the program
time.sleep(10)

# To fetch the data for one page
def scrape () :
  soup = bs(browser.page_source, "html.parser")
  for i in soup.find_all("ul", attrs={"class","expoplanet"}) :
    liTag = i.find_all("li")
    templist = []
    for index, li in enumerate (liTag) :
      if index == 0 :
        templist.append(li.find_all("a")[0].contents[0])
      else :
        try :
          templist.append(li.contents[0])
        except :
          templist.append("")
    hyperlinkTag = liTag[0]
    templist.append("https://exoplanets.nasa.gov/" + hyperlinkTag.find_all("a", href=True)[0]["href"])
    planetDataTemp.append(templist)
  browser.find_element_by_xpath("//*[@id='primary_column']/footer/div/div/div/nav/span[2]/a").click()

# To fetch the data for each planet
def scrapeSpecific (hyperlink) :
  page = requests.get(hyperlink)
  soup = bs(page.content, "html.parser")
  for tr in soup.find_all("tr", attrs={"class": "fact_row"}) :
    td = tr.find_all("td")
    templist = []
    for tdTag in td :
      try :
        templist.append(tdTag.find_all("div", attrs={"class": "value"})[0].contents[0])
      except :
        templist.append("")
    planetDataSpecific.append(templist)

scrape()

for p in planetDataTemp :
  scrapeSpecific(p[5])

for index, i in enumerate (planetDataTemp) :
  planetData.append(i + planetData[index])

with open ("final.csv", "w") as f :
  csvWriter = csv.writer(f)
  csvWriter.writerow(headers)
  csvWriter.writerows(planetData)