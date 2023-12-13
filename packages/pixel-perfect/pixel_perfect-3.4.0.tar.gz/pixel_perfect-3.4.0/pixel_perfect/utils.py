from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pixel_perfect import image_similarity 

# it can give any property like font-size, font, background-color and  color
def get_property_by_xpath(driver, location, property):
    element_property = driver.find_element(
        By.XPATH, location).value_of_css_property(property)
    return element_property

def get_image_aspect_ratio(driver, location):
    image_element = driver.find_element(By.XPATH, location)

    # Attempt to get aspect ratio from the "aspect-ratio" attribute
    aspect_ratio = driver.execute_script('return arguments[0].getAttribute("aspect-ratio");', image_element)

    # Attempt to get computed aspect ratio from CSS
    aspect_ratio_script = 'return window.getComputedStyle(arguments[0]).getPropertyValue("aspect-ratio");'
    computed_aspect_ratio = driver.execute_script(aspect_ratio_script, image_element)

    # Check which aspect ratio is valid and in the correct format
    if aspect_ratio and aspect_ratio.strip().lower() not in ('none', 'auto'):
        return aspect_ratio
    elif computed_aspect_ratio:
        return computed_aspect_ratio.replace(" ", "")
    else:
        # Return a default value or raise an exception if both are missing
        return None
    
def get_element_by_xpath(driver, location):
    element = driver.find_element(
        By.XPATH, location)
    return element

def get_text_by_xpath(driver, location):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, location)))
        actual_text = element.text
        return actual_text
    except:
        # If the element is not found, scroll to it using JavaScript
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, location)))
        return element.text

def get_count(driver, location):
    elements = driver.find_elements(By.XPATH, location)
    return len(elements)

def get_image_offset_ratio(driver, css_selector):
    script = f"const image = document.querySelector('{css_selector}'); return image.offsetWidth / image.offsetHeight;"
    offset_ratio = driver.execute_script(script)
    return offset_ratio

def get_image_offset_ratio_xpath(driver, xpath_selector):
    script = f"const image = document.evaluate('{xpath_selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return image.offsetWidth / image.offsetHeight;"
    offset_ratio = driver.execute_script(script)
    return offset_ratio

def click_element_by_xpath(driver, location):
    try:
        element = driver.find_element(By.XPATH, location)
        element.click()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_element_from_desktop(self, element_xpath):
    try:
        element = get_element_by_xpath(self.driver, element_xpath)
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        self.driver.set_window_size(1920,web_page_height)
        return element

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def get_element_from_tablet(self, element_xpath):
    try:
        element = get_element_by_xpath(self.driver, element_xpath)
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        self.driver.set_window_size(820,web_page_height)
        return element

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_element_from_mobile(self, element_xpath):
    try:
        element = get_element_by_xpath(self.driver, element_xpath)
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        self.driver.set_window_size(430,web_page_height)
        return element

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def take_screenshot(element, output_path):
    try:
        element_screenshot = element.screenshot_as_png
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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

def assert_elements_UI(expectedImage,actual_image):
        result = image_similarity(expectedImage, actual_image)
        assert result == True, f"Test has failed"

def take_screenshots_by_xpath(url, elements_xpaths, componentName, folder="baseline",screenSize='desktop'):
    if screenSize == 'desktop':
                for key, value in elements_xpaths.items():        
                    take_screenshot_by_xpath_in_desktop(url, value, key, componentName,folder)
    
    elif screenSize == 'mobile':
                for key, value in elements_xpaths.items():        
                    take_screenshot_by_xpath_in_mobile(url, value, key, componentName,folder)
    
    elif screenSize == 'tablet':
                for key, value in elements_xpaths.items():        
                    take_screenshot_by_xpath_in_tablet(url, value, key, componentName,folder)  
    
def take_screenshots_by_xpath_in_custom_screen_size(url, elements_xpaths, componentName,screen_height, screen_width,folder="baseline"):
    for key, value in elements_xpaths.items():        
        take_screenshot_by_xpath_in_custom_screen_size(url, value, key, componentName,folder,screen_height, screen_width)
    
def take_screenshot_by_xpath_in_desktop(url, element_xpath, element_name, componentName,folder="baseline"):
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

def take_screenshot_by_xpath_in_tablet(url, element_xpath, element_name, componentName,folder="baseline"):
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

def take_screenshot_by_xpath_in_mobile(url, element_xpath, element_name, componentName,folder="baseline"):
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

def take_screenshot_by_xpath_in_custom_screen_size(url, element_xpath, element_name, componentName, screenHeight, screenWidth,folder="baseline"):
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

def assert_elements_screenshots(self, url, section_xpaths, element_name, componentName, waitTime=3, folder="baseline",screenSize='desktop'):
        
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

def take_screenshot(self, url, section_xpaths, element_name, componentName, waitTime=3, folder="baseline",screenSize='desktop'):
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

def assert_elements_screenshots_in_custom_screen_size(self, url, section_xpaths, element_name, componentName,screenHeight, screenWidth, folder="baseline"):
        
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

def verify_element(element_name, componentName, folder="baseline", screenSize='desktop'):
    root_folder = f"{folder}/{componentName}/"
    print(f"Verify {componentName} - {element_name}")
    expectedImage = f"{root_folder}/{element_name}_{screenSize}_baseline.png"
    actual_image = f"{root_folder}/{element_name}_{screenSize}_actual.png"
    result = image_similarity(expectedImage, actual_image)
    assert result == True, f"{componentName} for {screenSize} has failed"

def capture_baselines(url, elements_xpaths, component_name, folder="baseline"):
    print(f"Capture baseline screenshot for {component_name}")
    take_screenshots_by_xpath(url, elements_xpaths, component_name, folder)

