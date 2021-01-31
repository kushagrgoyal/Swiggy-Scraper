import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# User Inputs
LOCATION = 'kothanur'
PATH = './chromedriver'

driver = webdriver.Chrome(PATH)

def if_all_unserviceable():
    all = driver.find_elements_by_id('all_restaurants')
        
    for a in all:
        print(a)

def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


driver.get('https://swiggy.com/')
driver.maximize_window()

location = driver.find_element_by_id('location')
location.send_keys(LOCATION)

try:
    location_sel = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_2W-T9')))
    location_sel.click()

    time.sleep(5)
    
    scroll(driver, 2) # Infinite Scrolling
    # driver.execute_script('window.scrollTo(0, 0)')
    
    # Restaurant Names
    rest_names = driver.find_elements_by_class_name('nA6kb')
    rest_names = [i.text for i in rest_names]

    # Cuisine Type
    c_names = []
    c_names = driver.find_elements_by_class_name('_1gURR')
    c_names = [i.text for i in c_names]

    # Rating, Delivery Times and Cost for Two
    ratings = []
    del_times = []
    cost_for_two = []
    extract_ratings = driver.find_elements_by_class_name('_3Mn31')
    for e_r in extract_ratings[:-1]:
        # value = e_r.find_element_by_tag_name('span')
        # ratings.append(value.text)
        
        info = e_r.find_elements_by_tag_name('div')
        info = [i.text for i in info]

        ratings.append(info[0])
        del_times.append(info[2])
        cost_for_two.append(info[4])
    
    print(c_names)
    print(len(rest_names), len(c_names), len(ratings), len(del_times), len(cost_for_two))
    print(rest_names)
    # all_data = {'Restaurant_Names':r_names, 'Cuisine_Type':c_names, 'Rating':ratings, 'Delivery_times': del_times, 'Cost_for_two':cost_for_two}
    # all_data = pd.DataFrame(all_data)
    # all_data.to_csv('Restaurants_currently_serving.csv')

finally:
    # time.sleep(5)
    driver.quit()