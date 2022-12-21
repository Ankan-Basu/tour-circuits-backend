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
import datetime

from pymongo import MongoClient
from pymongo import ASCENDING


def start_browser():
  chrome_options = Options()
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  driver = uc.Chrome(options=chrome_options)
  driver.get('https://google.com/travel') 
  return driver 


def get_top_sights(destination):

  driver = start_browser()
  search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@class="II2One j0Ppje zmMKJ LbIaRd"]'))
    )

  actions = ActionChains(driver)
  actions.send_keys_to_element(search_box, destination)
  actions.send_keys_to_element(search_box, Keys.ENTER)
  actions.perform()


  try:
    WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CLASS_NAME, 'kQb6Eb'))
      )
  except TimeoutException:
    print('Timeout', destination)
    driver.close()
    respDict = {
      'name': destination,
      'topPlaces': [],
      'timestamp': datetime.datetime.utcnow()
    }
    return respDict

  driver.execute_script('window.scrollTo(0, document.querySelector(\'.kQb6Eb\').scrollHeight);')

  top_sights = driver.find_elements(By.XPATH, '//div[@class="NnEw9 OBk50c T1Yjbc"]')

  results = []
  for sight in top_sights:

    place_img = sight.find_element(By.CLASS_NAME, 'R1Ybne').get_attribute('src')

    place_name = sight.find_element(By.XPATH, './/div[@class="skFvHc YmWhbc"]').text
    place_desc = sight.find_element(By.XPATH, './/div[@class="nFoFM"]').text
    place = place_img, place_name, place_desc
    results.append(place)

  driver.close()

  respArr = []
  for result in results:
    respJsonTmp = {
      "place": result[1],
      "desc": result[2],
      "image": result[0] 
    }
    respArr.append(respJsonTmp)

  # print(respJson)
  respDict = {
    'name': destination,
    'topPlaces': respArr,
    'timestamp': datetime.datetime.utcnow()
  }

  return respDict



def create_top_sights_data(db):
  top_sights_collection = db.top_sights
  places_collection = db.places

  places_cursor = places_collection.find()

  for place in places_cursor:
    place_name = place['name']
    respDict = get_top_sights(place_name)
    # print(respDict)
    db_resp = top_sights_collection.replace_one(
      {"name": place_name}, 
      respDict, 
      upsert = True
    )
    print(place_name, 'Data inserted', db_resp)


if __name__ == '__main__':

  client = MongoClient('mongodb://localhost:27017/')

  db = client.tours_database

  db.top_sights_collection.create_index([('name', ASCENDING)], unique=True)
  db.places_collection.create_index([('name', ASCENDING)], unique=True)

  create_top_sights_data(db)