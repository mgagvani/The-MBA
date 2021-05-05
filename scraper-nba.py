# scrape the niche.com site for colleges
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

#ts%

"""
if len(sys.argv) < 2:
    print("Provide the name of a state")
    sys.exit(1)

state = sys.argv[1]
print(state)
#state="georgia"
#launch url
"""
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
   

       
"""
        #Selenium visits each school
        schoolpage = driver.get(schoolurl)
        driver.implicitly_wait(20)
        
        #Selenium hands of the source of the specific school page
        soup_level2=BeautifulSoup(driver.page_source, 'lxml')
         
        schoolrecord=[]
      
        schoolinfo=soup_level2.find("h1", {"class":"postcard__title"})
        if schoolinfo != None:
          schoolname = schoolinfo.get_text(" | ").split("|")[0]
          schoolrecord.append(schoolname)

        studentinfo=soup_level2.find("section", {"id":"students"})
        if studentinfo != None:
          enrollment = studentinfo.get_text(" | ").split("|")[0:3] 
          schoolrecord.append(enrollment[2])
        else:
          schoolrecord.append("0")

        collegetype_list=soup_level2.find_all("a", {"class":"search-tags__wrap__list__tag__a"})
        for collegetype in collegetype_list: 
          if collegetype != None and "Public" in collegetype.get_text():
            schoolrecord.append("Public")
          elif collegetype != None and "Private" in collegetype.get_text():
            schoolrecord.append("Private")

        collegelink=soup_level2.find("a", {"class":"profile__website__link"})
        if collegelink !=None:
          collegeurl=collegelink.get('href')
          schoolrecord.append(collegeurl)
        else:
          schoolrecord.append("None")
     
        print(schoolrecord)
        datalist.append(schoolrecord)
        
        #Ask Selenium to click the back button
        driver.execute_script("window.history.go(-1)") 
        #end loop block for this page
    sys.exit(0)
        
    hasnextpage=soup_level1.find("li", {"class":"pagination__next"})
    if hasnextpage != None:
        currentpage +=1
        nexturl=url+"?page="+str(currentpage)
    else:
        morePages=False
            
        
    #loop has completed

#end the Selenium browser session
driver.quit()

#get current working directory
thedir='/d/dl/scraper/'

header = ['School', 'Enrollment', 'Type', 'URL']
with open( state + ".csv", "w", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header)
    for schoolrecord in datalist:
        writer.writerow(schoolrecord)
""" 
