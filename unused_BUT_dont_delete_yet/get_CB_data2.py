from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.aviationweather.gov/metar/data?ids=KSOP&format=raw&hours=0&taf=off&layout=on&date=0")

inputElement = driver.find_element_by_id("awc_main_content")
print(inputElement)

# ==================================

import urllib
from bs4 import BeautifulSoup

url = "https://www.aviationweather.gov/metar/data?ids=KSOP&format=raw&hours=0&taf=off&layout=on&date=0"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)
