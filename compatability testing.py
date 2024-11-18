import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def initialize_browser(browser_name):
    if browser_name == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.chrome.options import Options as ChromeOptions

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")  # Start maximized
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    elif browser_name == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    elif browser_name == "edge":
        driver_path = r"D:\Users\SBilal.ctr\Downloads\msedgedriver.exe"
        # Initialize Edge WebDriver using webdriver-manager for automatic management
        # Create Edge options
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")

        # Initialize Edge WebDriver with the path to the downloaded driver
        driver = webdriver.Edge(service=EdgeService(driver_path), options=edge_options)

    else:
        raise ValueError("Unsupported browser! Choose from 'chrome', 'firefox', 'edge'.")

    return driver


def read_credentials(filename):
    """
    Read login credentials from a CSV file.

    Args:
    - filename: The path to the CSV file containing credentials.

    Returns:
    - credentials: A list of dictionaries with username and password
    """
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        credentials = [row for row in reader]
    return credentials


def perform_test(driver, credentials):
    """
    Perform the login and functionality test.

    Args:
    - driver: The WebDriver instance to interact with the browser.
    - credentials: The login credentials to use for the test.

    Returns:
    - None
    """
    # Open the portal
    driver.get('https://qa-portal.somos.com/')
    driver.maximize_window()
    actual_title = driver.title
    expected_title = "Login | Somos"
    if actual_title == expected_title:
        print("Title Fetched Successfully")
    else:
        print("Title Fetch failed")
    time.sleep(2)

    # Extract credentials
    username = credentials[0]['username']
    password = credentials[0]['password']

    # Login
    username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "loginName")))
    username_field.send_keys(username)

    password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Password")))
    password_field.send_keys(password)

    login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ImgBtnSubmit']")))
    login_btn.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("Alert text:", alert.text)
    alert.accept()

    try:
        success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Welcome')]")
        print("Button clicked successfully, Somos Dashboard is being displayed:")
    except:
        print("Button click failed")
    time.sleep(5)

    # Navigate to "Number Admin History Report"
    numberadminhistory_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Number Admin History Report']")
    numberadminhistory_btn.click()

    numberadminhistory_search = driver.find_element(By.ID, "ctl00_CPHContent_TxtNumber")
    numberadminhistory_search.send_keys("8002089827")

    numberadminhistory_gobtn = driver.find_element(By.ID, "ctl00_CPHContent_ImgSumbit")
    numberadminhistory_gobtn.click()

    rows = driver.find_elements(By.XPATH,
                                "/html/body/form/div[3]/div/div[2]/div[2]/table/tbody/tr[1]/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/div/table/tbody/tr")
    if len(rows) >= 1:
        print("Number Administration History Report data Fetched Successfully")
    else:
        print("No Record(s) Found.")

    # Check the links on the page
    links = driver.find_elements(By.TAG_NAME, "a")

    # Initialize counters
    total_links = len(links)
    working_links = 0
    not_working_links = 0

    # Check each link
    for link in links:
        url = link.get_attribute("href")

        if url:  # Make sure the link is not None
            try:
                response = requests.head(url, allow_redirects=True)  # Use HEAD request to check status
                if response.status_code == 200:
                    print(f"Link is working: {url}")
                    working_links += 1
                else:
                    print(f"Link is broken (Status Code: {response.status_code}): {url}")
                    not_working_links += 1
            except requests.exceptions.RequestException as e:
                print(f"Link is broken (Error: {e}): {url}")
                not_working_links += 1

    # Print the summary
    print(f"\nTotal links: {total_links}")
    print(f"Working links: {working_links}")
    print(f"Not working links: {not_working_links}")


def main():
    # Define browsers to test
    browsers = ["chrome", "firefox", "edge"]

    # Load credentials from the CSV file
    credentials = read_credentials(r'D:\Users\SBilal.ctr\Downloads\credentials.csv')

    # Loop through each browser and run the test
    for browser in browsers:
        print(f"\nRunning test on {browser.capitalize()}...")
        driver = initialize_browser(browser)
        try:
            perform_test(driver, credentials)
        except Exception as e:
            print(f"Error occurred in {browser.capitalize()}: {e}")
        finally:
            driver.quit()


if __name__ == "__main__":
    main()
