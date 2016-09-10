import requests

url = "https://www.aviationweather.gov/metar/data?ids=KSOP&format=raw&hours=0&taf=off&layout=on&date=0"
res = requests.get(url)
text = res.text
find_me = "<!-- Data starts here -->"
beg_position_of_data = text.find(find_me) + 25
print(beg_position_of_data)
print(text[beg_position_of_data:beg_position_of_data + 50])
