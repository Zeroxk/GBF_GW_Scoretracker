from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from datetime import datetime
from time import sleep
import googlesheets
import pytz
import json

def findRecentlyActivePlayers(guildID):

    try:
        driver.get('{}#guild/detail/{}'.format(GBF_URL,guildID) )
        elements = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME,'prt-status-container')) 
        )
        val = elements[-1].find_element_by_class_name('prt-status-value').text

        return int(val)

    except Exception as err:
        print("Error when trying to find recently active players {}".format(err))
    
#TODO
def get_final_score(guildID, range_name):
    return

def main():

    '''Setup'''
    with open('config.json') as f:
        config = json.load(f)

    options = webdriver.ChromeOptions()
    profile_dir = config['profile_dir']
    if profile_dir != '':
        options.add_argument('user-data-dir={}'.format(profile_dir))

    global driver
    global GBF_URL
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(5)
    GBF_URL = config['gbf_url']
    GW_HOME_URL = GBF_URL + config['gw_partial_url']
    myGuildID = config['myGuildID']
    oppGuildID = config['oppGuildID']
    driver.get(GBF_URL)

    '''user logs in'''
    if profile_dir == '':
        input('Press enter to continue')
    
    driver.get(GW_HOME_URL)

    jst = pytz.timezone('Asia/Tokyo')
    start = datetime.now(jst).replace(hour=7, minute=0, second=0)
    end = datetime.now(jst).replace(hour=0, minute=0, second=0)
    
    googlesheets.setup(config['spreadsheetID'])

    now = datetime.now(jst)
    refreshInterval = int(config['refresh_interval'])

    while now.hour < start.hour:
        print("It's too early to start la, let me sleep for a minute more")
        sleep(60)
        now = datetime.now(jst)

    while now.hour > end.hour and now.hour >= start.hour:

        driver.refresh()
        myScore = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME,'txt-guild-point')) 
        )
        myScore = int( myScore.text.replace(',','') )

        oppScore = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME,'txt-rival-point')) 
        )
        oppScore = int( oppScore.text.replace(',','') )

        usOnline = findRecentlyActivePlayers(myGuildID)
        oppOnline = findRecentlyActivePlayers(oppGuildID)

        print('myScore: {}\toppScore: {}\tusOnline: {}\toppOnline: {}'.format(myScore,oppScore,usOnline,oppOnline))
        
        print('Current time: {}'.format(now.time()) )

        values = [
            [
                now.strftime('%H:%M:%S'), myScore, oppScore, usOnline, oppOnline
            ]
        ]

        googlesheets.write_to_sheet(values, config['sheet_range_name'])

        driver.get(GW_HOME_URL)
        sleep(refreshInterval)
        now = datetime.now(jst)

    get_final_score(oppGuildID, config['sheet_range_name'])

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print(Exception)
        raise