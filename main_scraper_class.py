import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Swiggy_scraper():    
    def __init__(self, driver, location, timeout, max_time_scroll):
        self.driver = driver
        self.location = location
        self.timeout = timeout
        self.max_time_scroll = max_time_scroll
    
    def start_with_location(self):
        self.driver.get('https://swiggy.com/')
        self.driver.maximize_window()

        location = self.driver.find_element_by_id('location')
        location.send_keys(self.location)
        
        location_sel = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_2W-T9')))
        location_sel.click()

        time.sleep(5)
    
    def scroll(self, rest_names, c_names, ratings, del_times, cost_for_two):
        scroll_pause_time = self.timeout
    
        # This line is needed to have the first 31 restaurants loaded before infinite scrolling starts
        rest_names, c_names, ratings, del_times, cost_for_two = self.extract_data()

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        start_time = time.time()
        while True:            
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height
            if time.time() - start_time >= self.max_time_scroll:
                break
    
    def extract_data(self):
        # Restaurant Names
        rest_names = self.driver.find_elements_by_class_name('nA6kb')
        rest_names = [i.text for i in rest_names]

        # Cuisine Type
        c_names = []
        c_names = self.driver.find_elements_by_class_name('_1gURR')
        c_names = [i.text for i in c_names]

        # Rating, Delivery Times and Cost for Two
        ratings = []
        del_times = []
        cost_for_two = []
        extract_ratings = self.driver.find_elements_by_class_name('_3Mn31')
        for e_r in extract_ratings[:-1]:            
            info = e_r.find_elements_by_tag_name('div')
            info = [i.text for i in info]

            ratings.append(info[0])
            del_times.append(info[2].split(' ')[0])
            cost_for_two.append(info[4].split(' ')[0])
        
        actual_length = self.find_actual_length(del_times)
        
        return rest_names[:actual_length], c_names[:actual_length], ratings[:actual_length], del_times[:actual_length], cost_for_two[:actual_length]
    
    def find_actual_length(self, arr):
        c = 0
        for i in arr:
            if i != '':
                c += 1
        return c
    
    def convert_to_csv(self, r, c, ra, dt, ct, save_path):
        data = {'Restaurant':r, 'Cuisine':c, 'Ratings':ra, 'Delivery_time_mins':dt, 'Cost_for_two':ct}
        data = pd.DataFrame(data)
        data.Cost_for_two = [i[1:] for i in data.Cost_for_two.values]
        data.to_csv(save_path)
        print('Data saved as a .csv file')
