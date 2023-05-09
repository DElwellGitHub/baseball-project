from time import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument('--headless')
    #Instantiate the Webdriver: Mention the executable parth of the webdriver you have downloaded
    # For linux/Mac
    driver = webdriver.Chrome(options = chrome_options)
    return driver

def getHeadlines(driver):
    driver.get(f'https://data.fivethirtyeight.com')
    # wait for element to load
    try:
        WebDriverWait(driver, 5).until(lambda s: s.find_element_by_id('dateIndex').is_displayed())
    except TimeoutException:
        print('TimeoutException: Element not found')
        return None

    #Step 2: Create a parse tree of page source after searching
    soup = BeautifulSoup(driver.page_source, lxml)
    #Step 3: Iterate over the search result and fetch the course
    for article in souplselect('tr.article'):
        for headline in article.select('td > a.article-title'):
            logging.info(f'{headline.text}')
        for timestamp in article.select('td{datetime}'):
            logging.info(f'{timestamp.text}')

# create the driver object.
driver = configure_driver()
getHeadlines(driver)
# close the driver.
driver.close()

print('hi there!')
