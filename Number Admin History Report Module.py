import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#service = Service(executable_path='https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.69/win64/chrome-win64.zip')
driver = webdriver.Chrome()
driver.get('https://qa-portal.somos.com/')
driver.maximize_window()
actual_title=driver.title
expected_title="Login | Somos"
if actual_title==expected_title:
    print("Title Fetched Successfully")
else:
    print("Title Fetched failed")
time.sleep(2)

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
try:
    # Wait for a specific element that should appear after the button is clicked
    success_message =driver.find_element(By.XPATH, "//*[contains(text(), 'Welcome')]")
    print("Button clicked successfully, Somos Dashboard is being displayed:")
except:
    print("Button click failed")

numberadminhistory_btn =driver.find_element(By.XPATH,"//span[normalize-space()='Number Admin History Report']")
numberadminhistory_btn.click()

numberadminhistory_search =driver.find_element(By.ID,"ctl00_CPHContent_TxtNumber")
numberadminhistory_search.send_keys("80020898275454545454")

numberadminhistory_gobtn =driver.find_element(By.ID,"ctl00_CPHContent_ImgSumbit")
numberadminhistory_gobtn.click()

rows=driver.find_elements(By.XPATH,"/html/body/form/div[3]/div/div[2]/div[2]/table/tbody/tr[1]/td/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/div/table/tbody/tr")
if len(rows) >= 2:
    print("Number Administration History Report data Fetched Successfully")
else:
    print("No Record(s) Found.")

# Find all hyperlinks on the page
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


# time.sleep(10)
# expected_title="Somos Portal Home Page | Somos"
# if actual_title==expected_title:
#     print("Billing Widget Opened Successfully")
# else:
#     print("Something went wrong")
time.sleep(5)
driver.close()

