import requests
import random

x = random.randint(1,26)
y = random.randint(1,26)
z = random.randint(1,26)

AI = ""
AI += "K"
AI += chr(64+x)
AI += chr(64+y)
AI += chr(64+z)
beg_url = 'https://www.aviationweather.gov/metar/data?ids='
end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'

count = 0
while count < 100:
    x = random.randint(1,26)
    y = random.randint(1,26)
    z = random.randint(1,26)

    AI = ""
    AI += "K"
    AI += chr(64+x)
    AI += chr(64+y)
    AI += chr(64+z)
    url = beg_url + AI + end_url
    res = requests.get(url)
    text = res.text
    find_beg = "<!-- Data starts here -->"
    find_end = "<br /><hr"
    beg_position_of_data = text.find(find_beg) + 25
    end_position_of_data = text.find(find_end)
    print(text[beg_position_of_data:end_position_of_data])

    count += 1

# url = "https://www.aviationweather.gov/metar/data?ids=KLAX&format=raw&hours=0&taf=off&layout=on&date=0"
# res = requests.get(url)
# text = res.text
# find_beg = "<!-- Data starts here -->"
# find_end = "<br /><hr"
# beg_position_of_data = text.find(find_beg) + 25
# end_position_of_data = text.find(find_end)
# print(text[beg_position_of_data:end_position_of_data])
