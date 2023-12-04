from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        self.driver = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.driver.quit()

    def test_write_post(self):
        try:
            self.driver.get(self.app_url)


            name_input = self.driver.find_element(By.XPATH, "//input[@name='name']")
            post_input = self.driver.find_element(By.XPATH, "//input[@name='post']")
            name_input.send_keys('John Doe')
            post_input.send_keys('This is a test post.')
            post_input.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'This is a test post')]"), 'This is a test post')
            )
            assert 'This is a test post' in self.driver.page_source
        except Exception as e:
            print(f"Exception in test_write_post: {e}")
            raise
    
    def test_write_empty_post(self):
        try:
            self.driver.get(self.app_url)
    
            name_input = self.driver.find_element(By.NAME, 'name')
            post_input = self.driver.find_element(By.NAME, 'post')
    
            name_input.send_keys('John Doe')
            post_input.send_keys(Keys.RETURN)
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='alert alert-danger']"), 'Message or comment cannot be blank.')
            )
            assert 'Message or comment cannot be blank.' in self.driver.page_source
    
        except Exception as e:
            print(f"Exception in test_write_empty_post: {e}")
            raise
    
    def test_write_post_and_comment(self):
        try:
            self.driver.get(self.app_url)
    
            name_input = self.driver.find_element(By.NAME, 'name')
            post_input = self.driver.find_element(By.NAME, 'post')
    
            name_input.send_keys('John Doe')
            post_input.send_keys('This is a test post.')
            post_input.send_keys(Keys.RETURN)
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'This is a test post')]"), 'This is a test post')
            )
            comment_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="comment"]')
            comment_input.send_keys('This is a test comment.')
            comment_input.send_keys(Keys.RETURN)
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='card-body']/blockquote/p"), 'This is a test comment.')
            )
    
            assert 'This is a test post' in self.driver.page_source
            assert 'This is a test comment.' in self.driver.page_source
    
        except Exception as e:
            print(f"Exception in test_write_post_and_comment: {e}")
            raise
    
    def test_write_post_with_category_and_use_filter(self):
        try:
            self.driver.get(self.app_url)
    
            name_input = self.driver.find_element(By.NAME, 'name')
            post_input = self.driver.find_element(By.NAME, 'post')
            categories_checkbox = self.driver.find_element(By.XPATH, "//input[@value='Secrets']")
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
            name_input.send_keys('John Doe')
            post_input.send_keys('This is a secret post.')
            categories_checkbox.click()
            submit_button.click()
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='card-body']/blockquote/p"), 'This is a secret post.')
            )
    
            secrets_filter_button = self.driver.find_element(By.CSS_SELECTOR, "button[value='Secrets']")
            secrets_filter_button.click()
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='card-body']/blockquote/p"), 'This is a secret post.')
            )
            assert 'This is a secret post.' in self.driver.page_source
    
        except Exception as e:
            print(f"Exception in test_write_post_with_category_and_use_filter: {e}")
            raise
    
    def test_write_post_and_search(self):
        try:
            self.driver.get(self.app_url)
    
            name_input = self.driver.find_element(By.NAME, 'name')
            post_input = self.driver.find_element(By.NAME, 'post')
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
            name_input.send_keys('John Doe')
            post_input.send_keys('This is a test post.')
            submit_button.click()
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='card-body']/blockquote/p"), 'This is a test post.')
            )
    
            search_input = self.driver.find_element(By.NAME, 'search')
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button#search_button")
    
            search_input.send_keys('test post')
            search_button.click()
    
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='card-body']/blockquote/p"), 'This is a test post.')
            )
    
            assert 'This is a test post.' in self.driver.page_source
    
        except Exception as e:
            print(f"Exception in test_write_post_and_search: {e}")
            raise

if __name__ == '__main__':
    unittest.main()
