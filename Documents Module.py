import csv
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to read credentials from CSV
def read_credentials(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        credentials = [row for row in reader]
    return credentials

# Load credentials
credentials = read_credentials(r'D:\Users\SBilal.ctr\Downloads\credentials.csv')
username = credentials[0]['username']
password = credentials[0]['password']

# Set up Chrome options
options = Options()
driver = webdriver.Chrome(service=Service(), options=options)

# Navigate to the login page
driver.get('https://qa-portal.somos.com/')  # Replace with your URL
driver.maximize_window()

# Enter login credentials
username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "loginName")))  # Replace with your field locator
username_field.send_keys(username)  # Correct usage

password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "Password")))  # Replace with your field locator
password_field.send_keys(password)  # Correct usage

# Click the login button
login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='ImgBtnSubmit']")))  # Replace with your button locator
login_btn.click()

WebDriverWait(driver, 10).until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert text:", alert.text)
alert.accept()

# Start the timer
start_time = time.time()
# Measure the time it took to load the page
end_time = time.time()

# Calculate the page load time
page_load_time = end_time - start_time;

print(f"Page load time: {page_load_time} seconds")

# Wait for a change on the page (e.g., a new element to appear)
try:
    success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Welcome')]")
    print("Button clicked successfully, Somos Dashboard is being displayed:")
except:
    print("Button click failed.")

# Find all hyperlinks on the page
# links = driver.find_elements(By.TAG_NAME, "a")

# Initialize counters
# total_links = len(links)
# working_links = 0
# not_working_links = 0

# Check each link
# for link in links:
#     url = link.get_attribute("href")
#
#     if url:  # Make sure the link is not None
#         try:
#             response = requests.head(url, allow_redirects=True)  # Use HEAD request to check status
#             if response.status_code == 200:
#                 print(f"Link is working: {url}")
#                 working_links += 1
#             else:
#                 print(f"Link is broken (Status Code: {response.status_code}): {url}")
#                 not_working_links += 1
#         except requests.exceptions.RequestException as e:
#             print(f"Link is broken (Error: {e}): {url}")
#             not_working_links += 1
#
# # Print the summary
# print(f"\nTotal links: {total_links}")
# print(f"Working links: {working_links}")
# print(f"Not working links: {not_working_links}")

billing_btn=driver.find_element(By.XPATH,"//p[contains(text(),'Search all accounts and view billing history, bala')]")
billing_btn.click()
# Step 1: Click the Documents button
documents_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Documents']"))
)
documents_btn.click()

# Step 2: Wait for the attachment input to be available
attachment_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='btnAddDocument']"))
)
attachment_btn.click()
attachment1_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='AsyncMFileUploadfile0']"))
)
attachment1_btn.click()
# Step 3: Provide the absolute file path
# file_path = r'D:\Users\SBilal.ctr\Downloads\credentials.csv'  # Use raw string to handle backslashes
#
# # Step 4: Upload the file
# attachment_btn.send_keys(file_path)
#
# # Optional: Wait to see the result of the upload
# WebDriverWait(driver, 10).until(
#     EC.text_to_be_present_in_element((By.ID, "some_result_element_id"), "Upload Successful")  # Change as needed
# )
# time.sleep(10)