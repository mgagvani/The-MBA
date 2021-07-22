from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import sqlite3
import pandas as pd
from pandas import DataFrame
import csv
import os, sys

season = "Playoffs"
year = "2019-20"
url = f"https://stats.nba.com/players/shooting/?Season={year}&SeasonType={season}&DistanceRange=By%20Zone"
print(url)

# create a new Chrome session
# driver = webdriver.Chrome()
profile = webdriver.FirefoxProfile()
# need this for https urls
profile.accept_untrusted_certs = True
driver = webdriver.Firefox(firefox_profile=profile)

datalist = [] #empty list
morePages = True
currentpage=1
nexturl=url

driver.implicitly_wait(60)
driver.get(nexturl)
print("Waiting for page to be loaded ...")
# This is an AJAX page, so while the page is loaded, the data takes a while to populate.  
element = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.CLASS_NAME, "nba-stat-table"))
)
players=[]
# create header.  Added totals in the last but one section.  It is hidden from display but the data is present
header = ['Name', 'URL', 'Team', 'Age','RestrictArea_FGM','RestrictArea_FGA','RestrictArea_FGpercent','Paint_FGM','Paint_FGA','Paint_FGpercent', 'MidRange_FGM','MidRange_FGA','MidRange_FGpercent','LeftCorner3_FGM','LeftCorner3_FGA','LeftCorner3_FGpercent','RightCorner3_FGM','RightCorner3_FGA','RightCorner3_FGpercent','Totals_FGM','Totals_FGA','Totals_FGpercent','AboveBreak3_FGM','AboveBreak3_FGA','AboveBreak3_FGpercent']

while morePages:

    soup_level1=BeautifulSoup(driver.page_source, 'lxml')
    #Beautiful Soup finds table with player stats for this page
    playertable = soup_level1.find('div', {"class":"nba-stat-table"})
    for link in playertable.find_all('td', {"class":"first"}):
        # iterate through all the <td> in this row
        parentrow = link.parent  # this gives us the row
        # There are multiple entries per player in the table, only use the ones that have more than 10 stats in the row
        rowstats = parentrow.find_all('td')
        if len(rowstats) > 10:
            currow = []
            rowisgood = True
            # Extract the player name and url
            playerurl = rowstats[0].find('a')['href']
            playername = rowstats[0].find('a').string
            teamname = rowstats[1].find('a').string
            currow.append(playername)
            currow.append(playerurl)
            currow.append(teamname)
            for rowstat in rowstats[2:]:
                nextcolval = rowstat.string
                # The way the AJAX page is designed, we still get a bunch of None entries in columns, move on..
                if nextcolval == None:
                    rowisgood = False
                    break
                if nextcolval.strip() == "-":
                    currow.append(0.0)
                else:
                    currow.append(float(nextcolval.strip()))
            if rowisgood == True:
                players.append(currow)

    hasnextpage=soup_level1.find("a", {"class":"stats-table-pagination__next"})
    if hasnextpage != None:
        if currentpage == 11:  # total 11 pages, hardcode, because too hard to figure out last page in Angular page
            morePages=False
            continue
        nextbutton = driver.find_elements_by_class_name('stats-table-pagination__next')[0]
        nextbutton.click()
        currentpage +=1

while morePages:

    soup_level1=BeautifulSoup(driver.page_source, 'lxml')
    #Beautiful Soup finds table with player stats for this page
    playertable = soup_level1.find('div', {"class":"nba-stat-table"})
    for link in playertable.find_all('td', {"class":"first"}):
        # iterate through all the <td> in this row
        parentrow = link.parent  # this gives us the row
        # There are multiple entries per player in the table, only use the ones that have more than 10 stats in the row
        rowstats = parentrow.find_all('td')
        if len(rowstats) > 10:
            currow = []
            rowisgood = True
            # Extract the player name and url
            playerurl = rowstats[0].find('a')['href']
            playername = rowstats[0].find('a').string
            teamname = rowstats[1].find('a').string
            currow.append(playername)
            currow.append(playerurl)
            currow.append(teamname)
            for rowstat in rowstats[2:]:
                nextcolval = rowstat.string
                # The way the AJAX page is designed, we still get a bunch of None entries in columns, move on..
                if nextcolval == None:
                    rowisgood = False
                    break
                currow.append(nextcolval.strip())
            if rowisgood == True:
                players.append(currow)

    hasnextpage=soup_level1.find("a", {"class":"stats-table-pagination__next"})
    if hasnextpage != None:
        if currentpage == 11:  # total 11 pages, hardcode, because too hard to figure out last page in Angular page
            morePages=False
            continue
        nextbutton = driver.find_elements_by_class_name('stats-table-pagination__next')[0]
        nextbutton.click()
        currentpage +=1
    else:
        morePages=False

print("Total number of players " + str(len(players)))
records = DataFrame(players, None, header)
records.to_csv('players.csv', index=False, header = True)

conn = sqlite3.connect('nba.db')
records.to_sql('PLAYERS', conn, if_exists='replace', index= True)

driver.quit()
   

       
