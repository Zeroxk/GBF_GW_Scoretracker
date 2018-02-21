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
import logging
import argparse

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

def find_scores():

    myScore = find_score('txt-guild-point')
    oppScore = find_score('txt-rival-point')

    scores = [myScore,oppScore]

    return scores

def find_score(class_name):

    score = WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located((By.CLASS_NAME,class_name)) 
            ).text
    score = int( score.replace(',','') ) if ',' in score else int(score) #Score with decimals is during a battle, without is from battle records

    return score

def is_strike_time():
    return driver.find_elements_by_class_name('img-rival-assault') != []

def get_values(now, myGuildID, oppGuildID):

    values = [now.strftime('%H:%M:%S')]

    scores = find_scores()
    values += scores

    usOnline = findRecentlyActivePlayers(myGuildID)
    oppOnline = findRecentlyActivePlayers(oppGuildID)
    values += [usOnline, oppOnline]

    print('myScore: {}\toppScore: {}\tusOnline: {}\toppOnline: {}'.format(values[1], values[2], values[3], values[4]))           
    print('Current time: {}'.format(now.time()) )

    return [values]

def main(args):

    '''Setup'''
    
    configFilename = args.configFile

    with open(configFilename) as f:
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
    sheet_range = config['sheet_range_name']

    now = datetime.now(jst)
    refreshInterval = int(config['refresh_interval'])

    while now.hour < start.hour:
        print("It's too early to start la, let me sleep for a minute more")
        sleep(60)
        now = datetime.now(jst)

    while now.hour > end.hour and now.hour >= start.hour:
        
        try:

            driver.refresh()
            print("Is it strike time? " + str(is_strike_time()) )
            values = get_values(now,myGuildID,oppGuildID)
            googlesheets.write_to_sheet(values, sheet_range)

            driver.get(GW_HOME_URL)
            sleep(refreshInterval)
            now = datetime.now(jst)

        except Exception as ex:
            print(e)
            continue
            
        

    #Wait until result screen for final score
    #TODO: Find better way to detect when battle result is ready, perhaps check for greyed out raid boxes
    if 'battle_result' not in driver.current_url:
        #sleep(1800)
        driver.refresh()

    #Find final score for most recent round
    driver.get(GW_HOME_URL)
    crewTab = driver.find_element_by_id((By.ID, 'tab-record'))
    driver.execute_script('arguments[0].scrollIntoView(true)', crewTab)
    crewTab.click()
    
    v = driver.find_elements_by_class_name('txt-guild-point')
    values = get_values(now,myGuildID,oppGuildID)
    googlesheets.write_to_sheet(values, sheet_range)

if __name__ == '__main__':

    logging.basicConfig(filename='main{}.log'.format(datetime.now().strftime('%d.%m.%Y')),level=logging.ERROR)

    try:
        parser = argparse.ArgumentParser(parents=[googlesheets.tools.argparser])
        parser.add_argument('-c', '--configFile', help='Sets config filename', default='config.json')

        args = parser.parse_args()
        main(args)
    except Exception as e:
        print(e)
        raise