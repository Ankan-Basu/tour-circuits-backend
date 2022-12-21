from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

def start_browser():
  chrome_options = Options()
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--no-sandbox") # linux only
  # chrome_options.add_argument("--headless")
  driver = uc.Chrome(options=chrome_options)
  # driver = webdriver.Chrome()
  driver.get('https://trivago.in') 
  return driver 

def enter_data(driver, destination):
  id = 'input-auto-complete'
  print('Start')
  search_box = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.ID, 'input-auto-complete'))
  )

  print('Search box found')


  # search_box.send_keys(u'ue007')

  # actions = ActionChains(driver)
  # actions.send_keys_to_element(search_box, destination)
  # actions.send_keys_to_element(search_box, Keys.ENTER)
  # actions.perform()

  check_in_button = driver.find_element(By.XPATH, '//button[@data-testid="calendar-checkin"]')
  
  print('Checkin button found')

  checkin_calenders_xpath = '//div[@class="grid w-full bg-grey-100 DatePickerQuickLinks_container__UPJER"]'


  # check_out_button = driver.find_element(By.XPATH, '//button[@data-testid="calendar-checkout"]')



  check_in_button.click()
  
  print('checkin button clicked')
  checkin_calenders = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, checkin_calenders_xpath))
  )
  print('Checkin calenders found')


  calenders_div = checkin_calenders.find_element(By.XPATH, './/div[@class="grid grid-cols-2 gap-10"]')

  print('Calenders found')

  calenders = calenders_div.find_elements(By.XPATH, './/div[@class="text-center"]')
  # print(calenders)
  
  check_in_month = calenders[0]

  checkin_date = check_in_month.find_element(By.XPATH, './/span[@class="absolute inset-0 flex justify-center items-center overflow-hidden -mt-px -ml-px border-grey-900 border border-solid rounded-l-xs"]')


  checkin_date.click()
  print('Date clicked')

  search_button = driver.find_element(By.XPATH, '//button[@data-testid="search-button"]')

  search_box.send_keys(destination)
  # time.sleep(1)
  suggestions_list = WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, '//div[@id="suggestion-list"]'))
  ) 
  search_box.send_keys(Keys.ENTER)
  search_button.click()

  print('Search button clicked')

  time.sleep(2)
  

  time.sleep(5)

  status_bar_xpath = '//div[@class="relative flex flex-row items-center h-13"]'
  no_of_res_xpath = '//span[@data-testid="loading-animation-accommodations-counter"]'
  #always present. gets filled with Stays found: after load
  hotels_list_xpath = '//ol[@data-testid="accommodation-list"]'

  '''
  <li class="py-1" data-testid="accommodation-list-element" data-accommodation="3853196">
  '''

  #subitem of hotels_list_xpath
  hotels_list_item_xpath = '//li[@class="py-1"]'
  hotels_list_item_xpath_alt = '//li[@data-testid="accommodation-list-element"]'


  '''
  <button type="button" data-testid="item-name" class="text-left w-full truncate font-bold"><span title="Tenzing Retreat" itemprop="name">Tenzing Retreat</span></button>
  '''
  hotel_title_area_xpath = '//button[@data-testid="item-name"]'
  hotel_title_area_xpath_alt = '//button[@class="text-left w-full truncate font-bold"]'

if __name__ == '__main__':
  driver = start_browser()
  destination = 'Sikkim'
  enter_data(driver, destination)
  driver.quit()

  # checkin_calenders_xpath = '//div[@class="grid w-full bg-grey-100 DatePickerQuickLinks_container__UPJER"]'

  # checkout_calenders_xpath = '//div[@class="grid w-full bg-grey-100 DatePickerQuickLinks_container__UPJER"]'


  # print(checkin_calenders_xpath == checkout_calenders_xpath)

# //div[@class="grid w-full bg-grey-100 DatePickerQuickLinks_container__UPJER"] checkout_cla