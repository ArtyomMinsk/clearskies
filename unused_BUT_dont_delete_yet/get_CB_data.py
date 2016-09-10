from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.aviationweather.gov/metar/data.com")

inputElement = driver.find_element_by_id("ids")
inputElement.send_keys('ksop')

inputElement.send_keys(Keys.ENTER)

# not needed.   The HTTP string is merely:

#       https://www.aviationweather.gov/metar/data?ids=KXYZ&format=raw&hours=0&taf=off&layout=on&date=0

#  .... replacing XYZ ( above ) with the airport identifier.
