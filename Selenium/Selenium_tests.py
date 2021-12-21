import pytest
import time
from selenium import webdriver

driver = webdriver.Edge()
driver.get('https://www.mvideo.ru')
search_box = driver.find_element_by_xpath('//*[@id="1"]')
driver.get_screenshot_as_file('OpenWebPage.png')
search_box.send_keys('Honor MagicBook 14\n')
driver.get_screenshot_as_file('SearchBox_input.png')
driver.find_element_by_xpath('/html/body/mvid-root/div/mvid-srp/mvid-layout/div/main/p')
driver.get_screenshot_as_file('SearchResult.png')
driver.quit()
