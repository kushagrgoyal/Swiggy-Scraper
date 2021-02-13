from main_scraper_class import *
import streamlit as st

# User Inputs
LOCATION = 'kothanur'
PATH = './chromedriver'
TIMEOUT = 4
MAX_TIME = 120
SAVE_PATH = 'Swiggy_scraped.csv'

# Initializing the Chrome Webdriver
driver = webdriver.Chrome(PATH)

# Scraping the data now
scraper = Swiggy_scraper(driver, LOCATION, TIMEOUT, MAX_TIME)
scraper.scrape_and_save(SAVE_PATH)
driver.quit()