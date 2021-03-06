#!/usr/bin/python3

# Author: twitter.com/spenkkkkk
# Tested on Linux
# Please download the driver you need and add it to your path 'e.x. ln -s /root/tools/geckodriver /usr/local/bin/geckodriver' or specify it in webdriver.Browser()
# Firefox driver = "https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"
# Chrome and Chromium driver = "https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip"

# Usage: python3 rapiddns.py target.com

import sys, os, threading, shutil, time
import pandas as pd
from selenium import webdriver


url = "https://rapiddns.io/subdomain/{}".format(sys.argv[1])
global driver

def main():

    try:
        if shutil.which("chrome") is not None:
            print("Chrome exists on system. Using it..")
            chrome()

        elif shutil.which("chromium") is not None:
            print("Chromium exists on system. Using it..")
            chrome()

        elif shutil.which("firefox") is not None:
            print("Firefox exists on system. Using it..")
            firefox()

        else:
            "We couldn't find a browser installed on your system."
            exit()

    except Exception as error:
        print(error)


def firefox():

    options = webdriver.firefox.options.Options()
    options.headless = True

    profile = webdriver.FirefoxProfile() 
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv,text/csv,text/comma-seperated-values,applicaiton/octet-stream")

    driver = webdriver.Firefox(firefox_profile=profile, options=options)
    driver.get(url)

    def gfg():
        print("Downloading csv file")
        driver.execute_script('exportData()')
      
    timer = threading.Timer(10.0, gfg) 
    timer.start()


def chrome():

    options = webdriver.chrome.options.Options()
    options.add_argument("download.default_directory={}".format(os.getcwd()))
    options.add_argument("--headless")  

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    print("Downloading csv file")
    driver.find_element_by_xpath('//button[text()="Export CSV"]').click()


def onlyDomains():

    import os.path
    file_path = "{}/{}.csv".format(os.getcwd(), sys.argv[1])

    while not os.path.exists(file_path):
        time.sleep(1)
        
    print("Sorting csv file and saving output to subdomains.txt")
    if os.path.isfile(file_path):
        df = pd.read_csv("{}.csv".format(sys.argv[1]))
        saved_column = df['Domain']

        for i in saved_column:
            with open ('domains-temp.txt', 'a') as temp:
                temp.write(i + '\n')

        lines_seen = set()
        outfile = open('subdomains.txt', 'w')

        for line in open('domains-temp.txt', 'r'):
            if line not in lines_seen:
                outfile.write(line)
                lines_seen.add(line)

        outfile.close()
        os.remove('domains-temp.txt')


if __name__ == "__main__":

    main()
    onlyDomains()
