from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver using ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open a webpage
    driver.get('https://www.example.com')

    # Get the title of the page
    title = driver.title
    print(f'Title of the page: {title}')
finally:
    # Close the WebDriver
    driver.quit()
