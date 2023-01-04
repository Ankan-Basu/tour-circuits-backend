from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from sys import argv, stdout
import json

import datetime

from pymongo import MongoClient
from pymongo import ASCENDING

def get_hotels(destination):
  try:
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(options=chrome_options)

    driver.get(f'https://google.com/travel/hotels/{destination}')
    # nav_links = driver.find_elements(By.XPATH, '//button[@class="VfPpkd-LgbsSe ksBjEc jcukd OXZ8S"]')

    # actions = ActionChains(driver)
    # actions.click(nav_links[4])
    # actions.perform()

    # time.sleep(5)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'l5cSPd'))
    )

    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'HlxIlc'))
    )

    '''
    <div class="uaTTDe BcKagd  bLc2Te Xr6b1e gEd38e" jscontroller="rqWJpd" jsaction="mouseover:nwdOcd; mouseout:pulEWc;z9B68b:bXptXb;GGrcWe:Lvnf5;rcuQ6b:npT2md;L64Xsb:s4bqYd;agoMJf:Xgd9s;hhT4le:yEOiIc;Ia9s:kKe0je;H692lc:zZBiUe;" data-hveid="47" jsname="mutHjb" jsmodel="JC21ye" data-is-promoted="true">
    '''
    hotel_item_class = 'uaTTDe'

    

    hotels_div = driver.find_element(By.XPATH, '//div[@class="l5cSPd"]')

    driver.execute_script('window.scrollTo(0, document.querySelector(\'.l5cSPd\').scrollHeight);')

    individual_hotel_items = hotels_div.find_elements(By.CLASS_NAME, "uaTTDe")

     

    resArr = []
    for individual_hotel_item in individual_hotel_items:
      # hotel_img = individual_hotel_item.find_element(By.XPATH, './/img[@class="x7VXS wnGtLb q5P4L"]')
      
      hotel_name = individual_hotel_item.find_element(By.XPATH, './/h2[@class="BgYkof ogfYpf ykx2he"]')

      try:
        hotel_features = individual_hotel_item.find_element(By.CLASS_NAME, 'HlxIlc')
      except NoSuchElementException:
        hotel_features = []
    
      try:
        hotel_price = individual_hotel_item.find_element(By.XPATH, './/a[@class="OxGZuc W8vlAc lRagtb"]')
      except NoSuchElementException:
        hotel_price = ''


      hotel_name = hotel_name.text
      if (hotel_features == []):
        pass
      else:
        hotel_features = hotel_features.text.split('\n')

      if (hotel_price == ''):
        pass
      else:
        hotel_price = hotel_price.text.split('\n')[-1]
      
      hotel_detail = {
        'hotel': hotel_name,
        'features': hotel_features,
        'price': hotel_price,
        'image': ''
      }

      # print (hotel_detail)
      resArr.append(hotel_detail)
      
    resObj = {
      'name': destination,
      'hotels': resArr,
      'timestamp': datetime.datetime.utcnow()
    }

    # print(resObj)

    driver.close()

    return resObj

  except:
    resObj = {
        'name': destination,
        'hotels': [],
        'status': 'err',
        'timestamp': datetime.datetime.utcnow()
    }
    print('err', resObj)
    return resObj


def create_hotels_data(db):
  hotels_collection = db.hotels
  places_collection = db.places

  places_cursor = places_collection.find()

  for place in places_cursor:
    place_name = place['name']
    respDict = get_hotels(place_name)
    # print(respDict)
    db_resp = hotels_collection.replace_one(
      {"name": place_name}, 
      respDict, 
      upsert = True
    )
    print(place_name, 'Data inserted', db_resp)
  

if __name__ == '__main__':
  mongoURL = 'mongodb+srv://devbros:2DevBros%40HITK@cluster0.5q9v57a.mongodb.net/?retryWrites=true&w=majority'
  client = MongoClient(mongoURL)

  db = client.tours_database

  db.hotels.create_index([('name', ASCENDING)], unique=True)
  db.places.create_index([('name', ASCENDING)], unique=True)
  # destination = argv[1]
  # get_top_places(driver, destination)

  # resp = get_hotels(destination)
  create_hotels_data(db)