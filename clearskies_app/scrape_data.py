import requests

url = "https://www.aviationweather.gov/metar/data?ids=KLAX&format=raw&hours=0&taf=off&layout=on&date=0"
res = requests.get(url)
text = res.text
find_beg = "<!-- Data starts here -->"
find_end = "<br /><hr"
beg_position_of_data = text.find(find_beg) + 25
end_position_of_data = text.find(find_end)
print(text[beg_position_of_data:end_position_of_data])


# break string up:
# first_part="https://www.aviationweather.gov/metar/data?ids="
# third_part="&format=raw&hours=0&taf=off&layout=on&date=0"
# middle_part  = " pass it an airport DUDE "
