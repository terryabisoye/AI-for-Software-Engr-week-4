import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def run_login_test(base_url, username, password, driver_path=None, screenshot_prefix="result"):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        if driver_path:
            from selenium.webdriver.chrome.service import Service
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"Failed to initialize WebDriver: {e}")
        return {"result": "error", "screenshot": None, "error": str(e)}
    
    try:
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)
        
        # Update these selectors to match YOUR page
        username_selector = 'input[name="username"]'
        password_selector = 'input[name="password"]'
        submit_selector = 'button[type="submit"]'
        success_indicator_selector = '.welcome'
        error_indicator_selector = '.error'
        
        # Wait for and interact with elements
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, username_selector)))
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.CSS_SELECTOR, password_selector)
        password_field.clear()
        password_field.send_keys(password)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
        submit_button.click()
        
        # Wait for page to process login
        time.sleep(2)  # Allow page transition
        
        screenshot_path = f"{screenshot_prefix}.png"
        driver.save_screenshot(screenshot_path)
        
        # Check result
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, success_indicator_selector)))
            result = "success"
        except TimeoutException:
            try:
                driver.find_element(By.CSS_SELECTOR, error_indicator_selector)
                result = "failure"
            except NoSuchElementException:
                result = "unknown"
        
        return {"result": result, "screenshot": screenshot_path}
    
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}")
        screenshot_path = f"{screenshot_prefix}_error.png"
        driver.save_screenshot(screenshot_path)
        return {"result": "timeout", "screenshot": screenshot_path, "error": str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        screenshot_path = f"{screenshot_prefix}_error.png"
        driver.save_screenshot(screenshot_path)
        return {"result": "error", "screenshot": screenshot_path, "error": str(e)}
    finally:
        driver.quit()


