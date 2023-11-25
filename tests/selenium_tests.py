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
      self.driver.get(self.app_url)
    
      name_input = self.driver.find_element('name', 'name')
      post_input = self.driver.find_element('name', 'post')
      #comment_input = self.driver.find_element('name', 'comment')
      comment_input = self.driver.find_element_by_css_selector('input[name="comment"]')

      name_input.send_keys('John Doe')
      post_input.send_keys('This is a test post.')
      comment_input.send_keys('This is a test comment.')
  
      post_input.send_keys(Keys.RETURN)
  
      time.sleep(2)
      assert 'This is a test post' in self.driver.page_source
      assert 'This is a test comment.' in self.driver.page_source

def test_write_post_with_category_and_use_filter(self):
    self.driver.get(app_url)

    name_input = self.driver.find_element('name', 'name')
    post_input = self.driver.find_element('name', 'post')
    categories_checkbox = self.driver.find_element_by_xpath("//input[@value='Secrets']")
    submit_button = self.driver.find_element_by_css_selector("button[type='submit']")

    name_input.send_keys('John Doe')
    post_input.send_keys('This is a secret post.')
    categories_checkbox.click()
    submit_button.click()

    time.sleep(2)

    secrets_filter_button = self.driver.find_element_by_css_selector("button[value='Secrets']")
    secrets_filter_button.click()

    time.sleep(2)
    assert 'This is a secret post.' in self.driver.page_source


if __name__ == '__main__':
  unittest.main()
