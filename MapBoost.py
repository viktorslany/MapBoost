import time
import math
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to generate random coordinates within a radius around a center point
def generate_random_coordinates(center_lat, center_lng, radius_km):
    radius_deg = radius_km / 111.12  # Approximately 1 degree latitude and longitude is approximately 111.12 km
    u = random.random()
    v = random.random()
    w = radius_deg * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    new_x = x / math.cos(center_lat)
    new_lng = new_x + center_lng
    new_lat = y + center_lat
    return new_lat, new_lng

# Loop for multiple iterations
for i in range(5):  # Change 5 to the desired number of iterations
    print(f"Iteration {i + 1}")

    # Start the Chrome web browser
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    options.add_argument("--disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-dev-shm-usage")  # Disable developer shared memory usage
    options.add_argument("--no-sandbox")  # Disable sandbox for Docker
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})  # Reject all cookies
    browser = webdriver.Chrome(options=options)

    # Open Google Maps
    browser.get("https://www.google.com/maps")

    # Find the search input field and type the search query
    search_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@autofocus="autofocus"]'))
    )
    search_box.send_keys("Viktor Slaný - Pojišťovací poradce pro Kooperativa pojišťovna, a.s.")
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load
    try:
        location_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Viktor Slaný - Pojišťovací poradce pro Kooperativa pojišťovna, a.s.")]'))
        )
        location_link.click()
    except:
        print("Location not found.")

    # Get the coordinates of the specified location
    time.sleep(5)  # Wait for the map to load
    current_url = browser.current_url
    lat_lng_start = current_url.split('@')[1].split(',')[0:2]
    lat_start, lng_start = map(float, lat_lng_start)

    # Generate random coordinates within a radius of 15 km from the specified location
    lat_dest, lng_dest = generate_random_coordinates(lat_start, lng_start, 15)

    # Set directions to the generated random destination
    time.sleep(5)  # Wait for the directions button to load
    directions_button = browser.find_element(By.XPATH, '//button[@data-value="Directions"]')
    directions_button.click()

    # Input the random destination
    destination_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Choose starting point, or click on the map..."]'))
    )
    destination_box.send_keys(f"{lat_dest}, {lng_dest}")
    destination_box.send_keys(Keys.RETURN)

    # Start navigating
    try:
        start_navigation_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-value="Start"]'))
        )
        start_navigation_button.click()
    except:
        print("Navigation button not found or clickable.")

    # End the navigation (just after starting for demonstration purposes)
    time.sleep(5)  # Simulate navigation
    try:
        end_navigation_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-value="End"]'))
        )
        end_navigation_button.click()
    except:
        print("End navigation button not found or clickable.")

    # Close the browser
    browser.quit()
