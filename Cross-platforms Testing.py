from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def test_layout_responsive(driver, url):
    # Define screen resolutions for mobile, tablet, and desktop
    resolutions = {
        'Mobile': (375, 667),  # mobile resolution (iPhone 6)
        'Tablet': (768, 1024),  # tablet resolution (iPad)
        'Desktop': (1366, 768)  # desktop resolution (1366x768)
    }

    # Open the DESIRED Website
    driver.get(url)
    driver.maximize_window()  # Start with the maximized window for testing

    # Test the layout for each screen size
    for device, (width, height) in resolutions.items():
        print(f"Testing layout for {device} ({width}x{height})...")
        driver.set_window_size(width, height)
        time.sleep(2)  # Wait for the layout to adjust

        # Check for layout changes:
        # Example checks - You can modify these based on your site
        try:
            if device == 'Mobile':
                # Example: Check for login button visibility (common in mobile layouts)
                menu = driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert menu.is_displayed(), f'login Button not visible on {device}'
                print(f"Mobile layout passed: login Button is visible.")
            elif device == 'Tablet':
                # Example: Check for tablet-specific navigation bar or footer adjustments
                menu = driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert menu.is_displayed(), f'login Button not visible on {device}'
                print(f"Mobile layout passed: login Button is visible.")
            else:
                # Example: Check for desktop layout consistency
                menu = driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert menu.is_displayed(), f'login Button not visible on {device}'
                print(f"Mobile layout passed: login Button is visible.")

        except Exception as e:
            print(f"Layout check failed for {device}: {str(e)}")

        time.sleep(1)  # Wait for the next test case to load properly


def main():
    # Set up the browser driver (Chrome in this case)
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        test_layout_responsive(driver, "https://qa-portal.somos.com")  # Replace with the URL of your site
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
