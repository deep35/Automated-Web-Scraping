# importing important libraries 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# loading chrome web browser
driver = webdriver.Chrome()
# main link of the website page
url = 'https://www.itsworthmore.com/'
# providing the website url to load to the browser
driver.get(url)

# to load the website in given time 
time.sleep(3)

# finding sell phone in web page    
cards = driver.find_element(By.ID,"main-page-view")
sell_phone_card = driver.find_element(By.XPATH, "//li[@class='lg-b lg-r md-b md-r sm-b sm-r same-height']")

# a sequence of actions to perform one after another
action = ActionChains(driver)

# function for the moving to the sell phone card
action.move_to_element(cards)
# click function to click the sell phone card
action.click(sell_phone_card)
# function to perform the actions 
action.perform()

# finding the Apple card in next page
phones_cards = driver.find_element(By.XPATH, "//ul[@id='main-page-view']")
# apple card is at the first position in the list 
apple = phones_cards.find_element(By.XPATH,"./li[1]")
# finding anchor tag to fetch the link of the next page which is Apple's page
apple = apple.find_element(By.XPATH,"./a[1]")
# fetched the link 
link = apple.get_attribute('href')
# update the link with the privious link 
url = link
# opening the next page by clicking the card contains link
apple.click()

# get the updated link to load to the browser
driver.get(url)

# finding the main block contains iphones cards
iphones = driver.find_element(By.ID,"main-page-view")
# finding the list tag of the main content
iphones = iphones.find_elements(By.XPATH,"./li") 
# storing all links of iphones
iphone_list=[]

# for loop for the fetching the links one by one
for i in range(0,len(iphones)):
    # fetching the link form the anchor tag
    iphone = iphones[i].find_element(By.XPATH,"./a[1]")
    # fetching the attribute which contains link of the card
    link = iphone.get_attribute('href')
    # storing in the list
    iphone_list.append(link)

# list for the fetched prices of iphones 
price = []

# function for the step by step automating and final price fetching
def price_fetch(url):
    # loading link of the iphone to the browser
    driver.get(url)
    # Wait for the page to load 
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='answer-1 first']")))

    # Click on the first option 
    brand_new = driver.find_element(By.XPATH, "//div[@class='answer-1 first']")
    brand_new.click()

    # Wait until the element is found and page is ready
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='button success right']")))

    # using this page will be scrolled to the element
    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

    # action chain to perform moving to the element and click it
    action = ActionChains(driver)
    action.move_to_element(next_button).click().perform()

    # added the wait time 
    time.sleep(5)
    
    # finding the class if it presents in page
    att = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='answer-1 first']")))

    # using this page will be scrolled to the element
    driver.execute_script("arguments[0].scrollIntoView(true);", att)
    
    # action chain to perform moving to the element and click it
    action = ActionChains(driver)
    action.move_to_element(att).click().perform()

    # Wait for page loading 
    time.sleep(5)

    # selecting the first option to the memory selection
    gb_256 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='answer-1 first']")))

    # using this page will be scrolled to the element
    driver.execute_script("arguments[0].scrollIntoView(true);", gb_256)

    # action chain to perform moving to the element and click it
    action = ActionChains(driver)
    action.move_to_element(gb_256).click().perform()

    # wait for loading the site
    time.sleep(5)
    # finding the final price section
    price = driver.find_element(By.CLASS_NAME, "your-offer").text
    # spliting it for fetching the price
    price = price.split('\n')
    # returning the price as string 
    return str(price[2])

# using the for loop fetching each iphons price 
for url in iphone_list:
    # calling the fetching function for the price fetching of this link 
    price_temp = price_fetch(url)
    # storing the price in list
    price.append(price_temp)

print(price)
# Convert the list into a pandas DataFrame
df = pd.DataFrame(price)

# Save the DataFrame to an Excel file
df.to_excel("price_list.xlsx", index=False,header=False)

# final wait before browser closes
time.sleep(5)
# Close the browser
driver.quit()