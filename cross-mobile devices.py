from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def test_layout_responsive(driver, url, resolutions):

    # Open the website
    driver.get(url)
    driver.maximize_window()  # Start with maximized window for testing

    # Test the layout for each screen size in the resolutions list
    for resolution in resolutions:
        width, height = resolution
        driver.save_screenshot(f"layout_{width}x{height}.png")
        print(f"Testing layout for {width}x{height} resolution...")

        # Resize the browser window to the specified resolution
        driver.set_window_size(width, height)
        time.sleep(2)  # Wait for the layout to adjust

        # Check for layout changes based on screen size:
        try:
            # Example checks based on the resolution
            if width <= 768:  # Typically mobile or small tablet
                # Check for the hamburger menu (mobile navigation)
                menu = driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert menu.is_displayed(), f'login Button not visible for {width}x{height}'
                print(f"Layout passed for {width}x{height}: login Button is visible.")
            elif width <= 1024:  # Tablet resolution
                # Check for tablet-specific navigation bar
                nav_bar = driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert nav_bar.is_displayed(), f'Tablet navigation not visible for {width}x{height}'
                print(f"Layout passed for {width}x{height}: Tablet navigation bar is visible.")
            else:  # Desktop resolution
                # Check for main content visibility
                main_content= driver.find_element(By.XPATH, "//input[@id='ImgBtnSubmit']")
                assert main_content.is_displayed(), f'Main content not visible for {width}x{height}'
                print(f"Layout passed for {width}x{height}: Main content is visible.")

        except Exception as e:
            print(f"Layout check failed for {width}x{height}: {str(e)}")

        time.sleep(1)  # Wait for the next test case to load properly


def main():
    # Define multiple screen resolutions to test
    resolutions = [
        (320, 480),  # Small mobile screen (e.g., older devices)
        (375, 667),  # Mobile screen (e.g., iPhone 6)
        (480, 800),  # Mobile resolution (e.g., Galaxy S3)
        (768, 1024),  # Tablet (e.g., iPad)
        (1024, 1366),  # Small desktop resolution
        (1366, 768),  # Standard desktop resolution (1366x768)
        (1440, 900),  # Larger desktop resolution (HD)
        (1920, 1080),  # Full HD desktop resolution (1080p)
        (2560, 1440),  # 2K resolution
        (3840, 2160)  # 4K resolution
    ]

    # Set up the browser driver (Chrome in this case)
    options = Options()

    driver = webdriver.Chrome(options=options)

    try:
        test_layout_responsive(driver, "https://qa-portal.somos.com", resolutions)  # Replace with your site's URL
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
