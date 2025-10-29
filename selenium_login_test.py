
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def run_login_test(base_url, username, password, driver_path=None, screenshot_prefix="result"):
    # Initialize Chrome WebDriver (assumes chromedriver in PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # run headless; remove for visible browser
    driver = webdriver.Chrome(options=options) if driver_path is None else webdriver.Chrome(executable_path=driver_path, options=options)

    try:
        driver.get(base_url)
        time.sleep(1)  # wait for page to load; prefer explicit waits in real tests

        # Example selectors (change these to match your page)
        username_selector = 'input[name="username"]'
        password_selector = 'input[name="password"]'
        submit_selector = 'button[type="submit"]'
        success_indicator_selector = '.welcome'  # element present after successful login
        error_indicator_selector = '.error'      # element present on failed login

        # Fill fields
        driver.find_element(By.CSS_SELECTOR, username_selector).clear()
        driver.find_element(By.CSS_SELECTOR, username_selector).send_keys(username)
        driver.find_element(By.CSS_SELECTOR, password_selector).clear()
        driver.find_element(By.CSS_SELECTOR, password_selector).send_keys(password)
        driver.find_element(By.CSS_SELECTOR, submit_selector).click()
        time.sleep(1)

        # Capture screenshot
        screenshot_path = f"{screenshot_prefix}.png"
        driver.save_screenshot(screenshot_path)

        # Check for success/error
        try:
            driver.find_element(By.CSS_SELECTOR, success_indicator_selector)
            result = "success"
        except NoSuchElementException:
            # No success indicator — check for error
            try:
                driver.find_element(By.CSS_SELECTOR, error_indicator_selector)
                result = "failure"
            except NoSuchElementException:
                result = "unknown"

        return {"result": result, "screenshot": screenshot_path}
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", required=True)
    parser.add_argument("--valid_user", required=True)
    parser.add_argument("--valid_pass", required=True)
    parser.add_argument("--invalid_user", default="baduser")
    parser.add_argument("--invalid_pass", default="badpass")
    args = parser.parse_args()

    print("Running valid-credentials test...")
    ok = run_login_test(args.base_url, args.valid_user, args.valid_pass, screenshot_prefix="login_valid")
    print(ok)

    print("Running invalid-credentials test...")
    bad = run_login_test(args.base_url, args.invalid_user, args.invalid_pass, screenshot_prefix="login_invalid")
    print(bad)



