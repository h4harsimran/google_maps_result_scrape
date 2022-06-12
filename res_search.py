# -*- coding: utf-8 -*-
"""
@author: harsi
"""

# importing libraries
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#input search criterion here
search_string = "restaurents in Brampton"


# Open browser
driver_path =r"chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path)
# Maximizing browser window to avoid hidden elements
driver.set_window_size(10000,10000)
driver.maximize_window()

# Opening google maps website
driver.get('https://www.google.com/maps?q=' 
           + search_string + "&start=" + str(0))

#%%

#define Database to store result values
# Title = Name of restaurent
# rating = Star rating of restaurent out of 5
# nor = Total number of reviews of restaurent
column_names=['Title','rating','nor','link']
res_data =pd.DataFrame(columns = column_names)

#%%%

#creating loop to scrape data
while True:
    #waiting to load
    time.sleep(3)
    
    #define loop to scroll the webpage to load all the restaurents on one page
    k=0
    while k<8:
        temp_res = driver.find_elements_by_xpath("//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
        action = ActionChains(driver)
        action.move_to_element(temp_res[(len(temp_res))-1]).perform()
        temp_res[(len(temp_res))-1].location_once_scrolled_into_view
        k+=1
        
    #waiting to load    
    time.sleep(3)
    
    #scrape result list from the results page
    res_list = driver.find_elements(By.CLASS_NAME,'Nv2PK.THOPZb.CpccDe')
    
    #loop to save data of each result in a dataframe
    for i in range(len(res_list)):
        try:
            #check for the required data and save it to dataframe. 
            #If no data available, continue to next iteration
            title=res_list[i].find_element(By.CSS_SELECTOR,'div.NrDZNb').text
            rating=res_list[i].find_element(By.CSS_SELECTOR,'span.MW4etd').text
            NOR=int(res_list[i].find_element(By.CSS_SELECTOR,'span.UY7F9').text.replace("(", "").replace(")", "").replace(",", ""))
            link=res_list[i].find_element(By.CSS_SELECTOR,'a.hfpxzc').get_attribute('href')
            temp_data=pd.DataFrame({'Title':[title],'rating':[rating],'nor':[NOR],'link':[link]})
            res_data=pd.concat([res_data, temp_data], ignore_index=True)
        except:
            continue
    try:
        #click on next page button to load next page of result. If button is disabled, break the loop.
        driver.find_element(By.ID,'ppdPk-Ej1Yeb-LgbsSe-tJiF1e').click()
    except:
        break
    
#%%%

#save data to a csv file
res_data=res_data.apply(pd.to_numeric, errors='ignore')
res_data = res_data.sort_values(by='nor', axis =0, ascending=False, ignore_index=True)
res_data.to_csv('res_data.csv',index=False)
