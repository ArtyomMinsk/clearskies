import requests


beg_url = 'https://www.aviationweather.gov/metar/data?ids='
end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'

mymin = 0
mymax = 1000
count = 0
places = Airfield.obects.all()

while mymin < count < mymax:

    for each in places:
        temp = places.indentifier
        tempp = list(temp)
        if tempp[0] != 'K':
            AI = temp
            url = beg_url + AI + end_url
            res = requests.get(url)
            text = res.text
            find_beg = "<!-- Data starts here -->"
            find_end = "<br /><hr"
            beg_position_of_data = text.find(find_beg) + 25
            end_position_of_data = text.find(find_end)
            if "No METAR found" not in text[beg_position_of_data:end_position_of_data]:
                print("FOUND ONE !!!!", text[beg_position_of_data:end_position_of_data])
    count += 1

# url = "https://www.aviationweather.gov/metar/data?ids=KLAX&format=raw&hours=0&taf=off&layout=on&date=0"
# res = requests.get(url)
# text = res.text
# find_beg = "<!-- Data starts here -->"
# find_end = "<br /><hr"
# beg_position_of_data = text.find(find_beg) + 25
# end_position_of_data = text.find(find_end)
# print(text[beg_position_of_data:end_position_of_data])
