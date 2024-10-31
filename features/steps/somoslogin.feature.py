from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup global driver
driver = None

@given('I am on the login page')
def step_given_i_am_on_the_login_page(context):
    global driver
    chrome_options = Options()
    service = Service(executable_path='https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.69/win64/chrome-win64.zip')  # Adjust the path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://qa-portal.somos.com/')  # Replace with the actual URL

@when('I enter valid credentials')
def step_when_i_enter_valid_credentials(context):
    def read_credentials(filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            credentials = [row for row in reader]
        return credentials

    # Load credentials
    credentials = read_credentials(r'D:\Users\SBilal.ctr\Downloads\credentials.csv')
    username = credentials[0]['username']
    password = credentials[0]['password']

    # Enter login credentials
    username_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "loginName")))  # Replace with your field locator
    username_field.send_keys(username)  # Correct usage

    password_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "Password")))  # Replace with your field locator
    password_field.send_keys(password)  # Correct usage

    # Click the login button
    login_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='ImgBtnSubmit']")))  # Replace with your button locator
    login_btn.click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("Alert text:", alert.text)
    alert.accept()

@then('I should see the dashboard')
def step_then_i_should_see_the_dashboard(context):
    try:
        # Wait for a specific element that should appear after the button is clicked
        success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Welcome')]")
        print("Button clicked successfully, Somos Dashboard is being displayed:")
    except:
        print("Button click failed")
    driver.quit()
