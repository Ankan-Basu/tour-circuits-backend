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


def start_browser():
  chrome_options = Options()
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox") # linux only
  # chrome_options.add_argument("--headless")
  driver = uc.Chrome(options=chrome_options)
  driver.get('https://google.com/travel') 
  return driver 


def get_top_places(driver, destination):
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
    print('Timeout')
    return

  driver.execute_script('window.scrollTo(0, document.querySelector(\'.kQb6Eb\').scrollHeight);')

  top_sights = driver.find_elements(By.XPATH, '//div[@class="NnEw9 OBk50c T1Yjbc"]')

  results = []
  for sight in top_sights:

    place_img = sight.find_element(By.CLASS_NAME, 'R1Ybne').get_attribute('src')

    place_name = sight.find_element(By.XPATH, './/div[@class="skFvHc YmWhbc"]').text
    place_desc = sight.find_element(By.XPATH, './/div[@class="nFoFM"]').text
    place = place_img, place_name, place_desc
    results.append(place)


  # with open('res.txt', 'w') as file:
  #   for result in results:
  #     file.write(f'Place: {result[1]}' + '\n')
  #     file.write(f'Desc: {result[2]}' +'\n')
  #     file.write(f'Img: {result[0]}' + '\n')
  #     file.write('\n')


  respArr = []
  for result in results:
    respJsonTmp = {
      "place": result[1],
      "desc": result[2],
      "image": result[0] 
    }
    respArr.append(respJsonTmp)

  # print(respJson)
  respJson = {
    'name': destination,
    'topPlaces': respArr
  }

  file = open('resp.json', 'w')
  json.dump(respJson, file)
  file.close()

# G5cKqf
# PH4Kgc QwCDkd
def get_hotels(destination):
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

  hotels_div = driver.find_element(By.XPATH, '//div[@class="l5cSPd"]')

  driver.execute_script('window.scrollTo(0, document.querySelector(\'.l5cSPd\').scrollHeight);')


  with open('test.html', 'w') as file:
    file.write(hotels_div.get_attribute('innerHTML'))

  hotel_names = hotels_div.find_elements(By.XPATH, './/h2[@class="BgYkof ogfYpf ykx2he"]')

  hotel_features = hotels_div.find_elements(By.CLASS_NAME, 'HlxIlc')
  
 
  hotel_prices = hotels_div.find_elements(By.XPATH, './/a[@class="OxGZuc W8vlAc lRagtb"]')


  results = []
  arr_len = len(hotel_names)


  for x in hotel_features:
    print(x.text, end='\n')
    print()

  for x in hotel_prices:
    print(x.text, end='\n')

  for x in hotel_names:
    print(x.text, end='\n')

  # for i in range(arr_len):
  #   result = {
  #     'hotelName': hotel_names[i].text, 
  #     # 'hotelFeatures': hotel_features[i].text, 
  #     'hotelPrice': hotel_prices[i].text
  #     }
  #   results.append(result)
    
  # for result in results:
  #   print(result, end='\n')
  #   print('\n')



def open_trivago():
  print('In func')
  chrome_options = Options()
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox") # linux only
  # chrome_options.add_argument("--headless")
  driver = uc.Chrome(options=chrome_options)

  print('created driver')

  driver.get(f'https://www.trivago.in/en-IN/lm/hotels-sikkim-india?search=200-64951;dr-20221123-20221124')

  time.sleep(10)
  driver.quit()



if __name__ == '__main__':
  # destination = input('Enter destination: ')
  driver = start_browser()
  # destination = 'Dajeeling'
  destination = argv[1]
  # get_top_places(driver, destination)

  get_hotels(destination)

  # open_trivago()
  # driver.quit()
