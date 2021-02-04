from main_scraper_class import *
import streamlit as st

# User Inputs
LOCATION = 'kothanur'
PATH = './chromedriver'
TIMEOUT = 2
MAX_TIME = 120
SAVE_PATH = 'Swiggy_scraped.csv'

driver = webdriver.Chrome(PATH)
rest_names = []
c_names = []
ratings = []
del_times = []
cost_for_two = []

# Scraping the data now
# Creating the scraper object
scraper = Swiggy_scraper(driver, LOCATION, TIMEOUT, MAX_TIME)

scraper.start_with_location()
scraper.scroll(rest_names, c_names, ratings, del_times, cost_for_two)

# Extract data
r, c, ra, dt, ct = scraper.extract_data()
rest_names.extend(r)
c_names.extend(c)
ratings.extend(ra)
del_times.extend(dt)
cost_for_two.extend(ct)

scraper.convert_to_csv(rest_names, c_names, ratings, del_times, cost_for_two, SAVE_PATH)
driver.quit()
print('Data saved as a .csv file')