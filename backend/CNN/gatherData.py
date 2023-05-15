from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import requests
import os

# Set the URL to fetch
url = "http://192.168.75.202:8080/videomgr.html#/photo"

# Set the directory to save the images to
directory = r"D:\priv\Programming\ARCV2\Training"

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the URL
driver.get(url)

# Wait for the page to load
time.sleep(2)

# Find all the <a> tags with href attribute that starts with '/v/photo/photo'
a_tags = driver.find_elements(By.XPATH, '//a[starts-with(@href, "/v/photo/photo")]')

# Loop through each <a> tag and download the image
for i, a_tag in enumerate(a_tags):
    # Get the href attribute and extract the image filename
    href = a_tag.get_attribute('href')
    filename = href.split('/')[-1]

    # Construct the full image URL
    img_url = href

    # Save the image to the local file system
    filepath = os.path.join(directory, filename)
    response = requests.get(img_url)

    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print("Saved image:", filename)
    else:
        print("Failed to download image:", filename)

# Close the browser
driver.quit()
