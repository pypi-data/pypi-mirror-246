from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pixel_perfect import image_similarity 
from pixel_perfect import get_element_by_xpath 

def take_screenshots(url, elements_xpaths, componentName, folder="baseline",screenSize='desktop'):
    if screenSize == 'desktop':
                for key, value in elements_xpaths.items():        
                    take_screenshot_desktop(url, value, key, componentName,folder)
    
    elif screenSize == 'mobile':
                for key, value in elements_xpaths.items():        
                    take_screenshot_mobile(url, value, key, componentName,folder)
    
    elif screenSize == 'tablet':
                for key, value in elements_xpaths.items():        
                    take_screenshot_tablet(url, value, key, componentName,folder)  
    
def take_screenshots_custom_screen_size(url, elements_xpaths, componentName,screen_height, screen_width,folder="baseline"):
    for key, value in elements_xpaths.items():        
        take_screenshot_in_custom_screen_size(url, value, key, componentName,folder,screen_height, screen_width)
    
def take_screenshot_desktop(url, element_xpath, element_name, componentName,folder="baseline"):
    try:
        baseline_tc_folder =  f"{folder}/{componentName}/"
        os.makedirs(baseline_tc_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
        driver = webdriver.Chrome(options=options)
        vars = {}
        driver.get(url)
        time.sleep(2)
        element = get_element_by_xpath(driver, element_xpath)
        web_page_height = driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        driver.set_window_size(1920,web_page_height)

        time.sleep(3)
        element_screenshot = element.screenshot_as_png
        output_path = f"{baseline_tc_folder}/{element_name}_desktop_baseline.png"
 
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def take_screenshot_tablet(url, element_xpath, element_name, componentName,folder="baseline"):
    try:
        baseline_tc_folder =  f"{folder}/{componentName}/"
        os.makedirs(baseline_tc_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=820,1180")

        driver = webdriver.Chrome(options=options)
        vars = {}
        driver.get(url)
        time.sleep(2)
        element = get_element_by_xpath(driver, element_xpath)
        web_page_height = driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        driver.set_window_size(820,web_page_height)

        time.sleep(3)
        element_screenshot = element.screenshot_as_png
        output_path = f"{baseline_tc_folder}/{element_name}_tablet_baseline.png"
 
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def take_screenshot_mobile(url, element_xpath, element_name, componentName,folder="baseline"):
    try:
        baseline_tc_folder =  f"{folder}/{componentName}/"
        os.makedirs(baseline_tc_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=430,932")

        driver = webdriver.Chrome(options=options)
        vars = {}
        driver.get(url)
        time.sleep(2)
        element = get_element_by_xpath(driver, element_xpath)
        web_page_height = driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        driver.set_window_size(430,web_page_height)

        time.sleep(3)
        element_screenshot = element.screenshot_as_png
        output_path = f"{baseline_tc_folder}/{element_name}_mobile_baseline.png"
 
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def take_screenshot_in_custom_screen_size(url, element_xpath, element_name, componentName, screenHeight, screenWidth,folder="baseline"):
    try:
        baseline_tc_folder =  f"{folder}/{componentName}/"
        os.makedirs(baseline_tc_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
    
        driver = webdriver.Chrome(options=options)
        vars = {}
        driver.get(url)
        time.sleep(2)
        element = get_element_by_xpath(driver, element_xpath)
        web_page_height = driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        driver.set_window_size(screenWidth,web_page_height)

        time.sleep(3)
        element_screenshot = element.screenshot_as_png
        output_path = f"{baseline_tc_folder}/{element_name}_{screenWidth}X{screenHeight}_baseline.png"
 
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def capture_baselines(url, elements_xpaths, component_name, folder="baseline",screenSize='desktop'):
    print(f"Capture baseline screenshot for {component_name}")
    take_screenshots(url, elements_xpaths, component_name, folder, screenSize)

