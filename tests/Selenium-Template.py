from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import time
import unittest

class SystemTest(unittest.TestCase):
  def setUp(self):
    display = Display(visible=0, size=(800, 800))  
    display.start()
    
    chromedriver_autoinstaller.install() 
    chrome_options = webdriver.ChromeOptions()    
    options = [
       "--window-size=1200,1200",
        "--ignore-certificate-errors"
     ]
    for option in options:
        chrome_options.add_argument(option)
    self.app_url = 'http://127.0.0.1:5000'
    self.driver = webdriver.Chrome(options = chrome_options)
    
  def tearDown(self):
    self.driver.quit()

  def test_write_post_and_comment(self):
      driver.get(self.app_url)
    
      name_input = driver.find_element_by_name('name')
      post_input = driver.find_element_by_name('post')
      comment_input = driver.find_element_by_name('comment')
  
      name_input.send_keys('John Doe')
      post_input.send_keys('This is a test post.')
      comment_input.send_keys('This is a test comment.')
  
      post_input.send_keys(Keys.RETURN)
  
      time.sleep(2)
      assert 'Wrong Text' in driver.page_source
      assert 'This is a test comment.' in driver.page_source
