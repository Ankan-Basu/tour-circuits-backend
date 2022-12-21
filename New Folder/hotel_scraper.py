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

def get_hotels(destination):
  chrome_options = Options()
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox") # linux only
  # chrome_options.add_argument("--headless")
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
  # print(hotels_item)


  # with open('test.html', 'w') as file:
  #   file.write(hotels_div.get_attribute('innerHTML'))

  for individual_hotel_item in individual_hotel_items:
    print('Inside loop')
    hotel_name = individual_hotel_item.find_elements(By.XPATH, './/h2[@class="BgYkof ogfYpf ykx2he"]')

    print(len(hotel_names), len(hotels_item))

    hotel_features = individual_hotel_item.find_elements(By.CLASS_NAME, 'HlxIlc')
    
  
    hotel_price = individual_hotel_item.find_elements(By.XPATH, './/a[@class="OxGZuc W8vlAc lRagtb"]')


  results = []
  arr_len = len(hotel_names)


  # for x in hotel_features:
  #   print(x.text, end='\n')
  #   print()

  # for x in hotel_prices:
  #   print(x.text, end='\n')

  # for x in hotel_names:
  #   print(x.text, end='\n')

  

if __name__ == '__main__':
  # destination = input('Enter destination: ')
  # driver = start_browser()
  # destination = 'Dajeeling'
  destination = argv[1]
  # get_top_places(driver, destination)

  get_hotels(destination)

  # open_trivago()
  # driver.quit()