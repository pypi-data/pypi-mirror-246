from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pixel_perfect import image_similarity

def get_element_by_xpath(driver, location):
    element = driver.find_element(
        By.XPATH, location)
    return element

def get_baseline_loc(element_name, componentName,screenSize='desktop', folder="baseline"):
        root_folder = f"{folder}/{componentName}/"
        os.makedirs(root_folder, exist_ok=True)
        expectedImage = f"{root_folder}/{element_name}_{screenSize}_baseline.png"        
        return expectedImage

def get_actual_loc(element_name, componentName,screenSize='desktop', folder="baseline"):
        root_folder = f"{folder}/{componentName}/"
        os.makedirs(root_folder, exist_ok=True)
        actual_image = f"{root_folder}/{element_name}_{screenSize}_actual.png"
        return actual_image

def capture_assert_screenshots(self, url, section_xpaths, element_name, componentName, waitTime=3, folder="baseline",screenSize='desktop'):
        
        root_folder = f"{folder}/{componentName}/"
        self.driver.get(url)
        time.sleep(3)
 
        print(f"Verify {componentName} - {element_name}")

        expectedImage = f"{root_folder}/{element_name}_{screenSize}_baseline.png"
        actual_image = f"{root_folder}/{element_name}_{screenSize}_actual.png"

        contact_us_section = get_element_by_xpath(self.driver, section_xpaths[element_name])
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        if screenSize == 'tablet':
            screenWidth = 820

        elif screenSize == 'mobile':
            screenWidth = 430
        else:
            screenWidth = 1920   

        self.driver.set_window_size(screenWidth,web_page_height)

        time.sleep(waitTime)
        element_screenshot = contact_us_section.screenshot_as_png
        with open(actual_image, "wb") as file:
            file.write(element_screenshot)

        result = image_similarity(expectedImage, actual_image)
        assert result == True, f"{componentName} for {screenSize} has failed"

def capture_screenshot(self, url, section_xpaths, element_name, componentName, waitTime=3, folder="baseline",screenSize='desktop'):
        root_folder = f"{folder}/{componentName}/"
        self.driver.get(url)
        time.sleep(3)
        print(f"Verify {componentName} - {element_name}")
        actual_image = f"{root_folder}/{element_name}_{screenSize}_actual.png"

        contact_us_section = get_element_by_xpath(self.driver, section_xpaths[element_name])
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        if screenSize == 'tablet':
            screenWidth = 820

        elif screenSize == 'mobile':
            screenWidth = 430
        else:
            screenWidth = 1920   

        self.driver.set_window_size(screenWidth,web_page_height)

        time.sleep(waitTime)
        element_screenshot = contact_us_section.screenshot_as_png
        with open(actual_image, "wb") as file:
            file.write(element_screenshot)

def capture_assert_screenshots_in_custom_screen_size(self, url, section_xpaths, element_name, componentName,screenHeight, screenWidth, folder="baseline"):
        
        root_folder = f"{folder}/{componentName}/"
        self.driver.get(url)
        time.sleep(3)
 
        print(f"Verify {componentName} - {element_name}")

        expectedImage = f"{root_folder}/{element_name}_{screenWidth}X{screenHeight}_baseline.png"
        actual_image = f"{root_folder}/{element_name}_{screenWidth}X{screenHeight}_actual.png"

        contact_us_section = get_element_by_xpath(self.driver, section_xpaths[element_name])
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        self.driver.set_window_size(screenWidth,web_page_height)

        time.sleep(2)
        element_screenshot = contact_us_section.screenshot_as_png
        with open(actual_image, "wb") as file:
            file.write(element_screenshot)

        result = image_similarity(expectedImage, actual_image)
        assert result == True

def verify_screenshot(element_name, componentName, folder="baseline", screenSize='desktop'):
    root_folder = f"{folder}/{componentName}/"
    print(f"Verify {componentName} - {element_name}")
    expectedImage = f"{root_folder}/{element_name}_{screenSize}_baseline.png"
    actual_image = f"{root_folder}/{element_name}_{screenSize}_actual.png"
    result = image_similarity(expectedImage, actual_image)
    assert result == True, f"{componentName} for {screenSize} has failed"
