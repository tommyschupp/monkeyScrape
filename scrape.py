#type the following into your cmd
#pip install pandas
#pip install futures
#pip install beautifulsoup4
#pip install -U selenium

#download chromedriver from here https://chromedriver.chromium.org/
#put chromedriver.exe into the SAME FOLDER AS this file and the csv files

import pandas 
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

eyList = pandas.read_csv('MaleMonkey.csv')['values']
etteList = pandas.read_csv('FemaleMonkey.csv')['values']
eyOwnerList = []
etteOwnerList = []
sharedList = []

def eyScrape(address):
    chromeOptions = Options()
    #chromeOptions.add_argument('--headless') #uncomment this to make selenium headless
    driver = webdriver.Chrome(options=chromeOptions)
    url = 'https://explorer.solana.com/address/' + address + '/largest'
    driver.get(url)
    driver.maximize_window()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for addressLink in soup.find_all('a', class_="text-truncate address-truncate"):
        if(addressLink.parent.parent.parent.next_sibling.string == "1"):
            print(addressLink.contents[0])
            eyOwnerList.append(addressLink.contents[0])
            break

def etteScrape(address):
    chromeOptions = Options()
    #chromeOptions.add_argument('--headless') #uncomment this to make selenium headless
    driver = webdriver.Chrome(options=chromeOptions)
    url = 'https://explorer.solana.com/address/' + address + '/largest'
    driver.get(url)
    driver.maximize_window()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for addressLink in soup.find_all('a', class_="text-truncate address-truncate"):
        if(addressLink.parent.parent.parent.next_sibling.string == "1"):
            print(addressLink.contents[0])
            etteOwnerList.append(addressLink.contents[0])
            break
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=30) as executor:
        for address in eyList:
            executor.submit(eyScrape, address)
        for address in etteList:
            executor.submit(etteScrape, address)

for address in eyOwnerList:
    if address in etteOwnerList:
        sharedList.append(address)

results = pandas.DataFrame(list(sharedList), columns=["Owner"])
results.to_csv(r'results.csv', index = False, header = True)


