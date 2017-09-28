from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import sleep
import googlesheets
import pytz

def findRecentlyActivePlayers(guildID):
    driver.get(GBF_URL + '#guild/detail/{}'.format(guildID) )
    elements = driver.find_elements_by_class_name('prt-status-container')
    val = elements[-1].find_element_by_class_name('prt-status-value').text
    print('val: {}'.format(val))
    return int(val)

def main():

    '''Setup'''
    options = webdriver.ChromeOptions()
    global driver
    global GBF_URL
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(5)
    GBF_URL = 'http://game.granbluefantasy.jp/'
    GW_HOME_URL = GBF_URL + '#event/teamraid033'
    myGuildID = '147448'
    oppGuildID = '137217'
    driver.get(GBF_URL)

    '''user logs in'''
    input('Press enter to continue')

    driver.get(GW_HOME_URL)

    jst = pytz.timezone('Asia/Tokyo')
    start = datetime.now(jst).replace(hour=7, minute=0, second=0)
    end = datetime.now(jst).replace(hour=0, minute=0, second=0)
    
    now = datetime.now(jst)
    refreshInterval = 600
    
    while now.hour > end.hour and now.hour >= start.hour:
        myScore = driver.find_element_by_class_name('txt-guild-point').text.replace(',','')
        oppScore = driver.find_element_by_class_name('txt-rival-point').text.replace(',','')

        usOnline = 0
        oppOnline = 0

        print('myScore: {}\toppScore: {}\tusOnline: {}\toppOnline: {}'.format(myScore,oppScore,usOnline,oppOnline))
        
        print('Current time: {}'.format(now.time()) )
        googlesheets.write_to_sheet(int(myScore), int(oppScore), now.strftime('%H:%M:%S'), usOnline, oppOnline)

        sleep(refreshInterval)
        now = datetime.now(jst)
        driver.refresh()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print(Exception)
        raise