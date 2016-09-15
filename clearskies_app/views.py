from django.shortcuts import render
from django.http import HttpResponse
from .models import Airfield
from numpy import arange
import requests


def home(request):
    return render(request, 'clearskies_app/index.html', context=None)


def plan(request):
    airfields = Airfield.objects.all()
    return render(request, 'clearskies_app/plan.html', {'airfields': airfields})


def get_corridor_airports(st, fin):
    airport_weather = []
    start = Airfield.objects.get(identifier=st)
    wx = get_data(start.identifier)
    if wx:
        airport_weather.append((start, wx))
    finish = Airfield.objects.get(identifier=fin)
    startLAT = start.latitude
    startLON = start.longitude
    finishLAT = finish.latitude
    finishLON = finish.longitude
    # print("startLAT", startLAT, "startLON", startLON, "finishLAT", finishLAT, "finishLON", finishLON)
    # print("*********")
    if startLAT < finishLAT:
        x1 = startLAT
        x2 = finishLAT
    else:
        x2 = startLAT
        x1 = finishLAT
    if startLON < finishLON:
        y1 = startLON
        y2 = finishLON
    else:
        y2 = startLON
        y1 = finishLON
    # check for min width
    if x2 - x1 < 1.0:
        short = (1-(x2-x1))/2
        x1 -= short
        x2 += short

    if y2 - y1 < 1.0:
        short = (1-(y2-y1))/2
        y1 -= short
        y2 += short

    selected_airports = Airfield.objects.filter(latitude__gte=x1,
                                                latitude__lte=x2,
                                                longitude__gte=y1,
                                                longitude__lte=y2)
    # print("selected_airports: ", *selected_airports, sep='\n')
    # print(len(selected_airports))
    lat_diff = abs(startLAT - finishLAT)
    lon_diff = abs(startLON - finishLON)
    if lon_diff > lat_diff:
        ratio = lat_diff / (lon_diff * 10)
        step_thru = "lon"
        # avg_stations = round(lon_diff)
        if startLON < finishLON:
            increment = 0.1
            extend = 0.4
        else:
            increment = -0.1
            extend = -0.4
    else:
        ratio = lon_diff / (lat_diff * 10)
        step_thru = "lat"
        # avg_stations = round(lat_diff)
        if startLAT < finishLAT:
            increment = 0.1
            extend = 0.4
        else:
            increment = -0.1
            extend = -0.4

    count = 1  # delete when testng done

    if step_thru == "lon":
        startP = startLON
        finishP = finishLON
    else:
        startP = startLAT
        finishP = finishLAT

    for i in arange(startP, finishP + extend, increment):
        for each_airport in selected_airports:
            if step_thru == 'lon':
                if each_airport.latitude <= startLAT + 0.4 and each_airport.latitude >= startLAT - 0.4 and each_airport.longitude <= i and each_airport.longitude >= i - 0.1:
                    # print("LAT = ", each_airport.latitude, "    LON = ", each_airport.longitude)
                    if startLAT > finishLAT:
                        startLAT -= ratio
                    else:
                        startLAT += ratio
                    # print("LAT-SUCCESS!!!!!", each_airport, each_airport.latitude, each_airport.longitude, count)
                    wx = get_data(each_airport.identifier)
                    if wx:
                        airport_weather.append((each_airport, wx))
                    count += 1

            elif step_thru == 'lat':
                if each_airport.longitude <= startLON + 0.4 and each_airport.longitude >= startLON - 0.4 and each_airport.latitude <= i and each_airport.latitude >= i - 0.1:
                    # print("LAT = ", each_airport.latitude, "    LON = ", each_airport.longitude)
                    if startLON > finishLON:
                        startLON -= ratio
                    else:
                        startLON += ratio
                    # print("LON-SUCCESS!!!!!", each_airport, each_airport.latitude, each_airport.longitude, count)
                    wx = get_data(each_airport.identifier)
                    if wx:
                        airport_weather.append((each_airport, wx))
                    count += 1

    wx = get_data(finish.identifier)
    if wx:
        airport_weather.append((finish, wx))
    dup = len(airport_weather) - 1
    # print(dup)
    for i in range(dup, 0, -1):
        if airport_weather[i] == airport_weather[i-1] or airport_weather[i] == airport_weather[i-2]:
            airport_weather.pop(i)
            # print("GOT POPPED !!!!!!!")
    # print(airport_weather, "WWWWWWWWWW")
    return airport_weather


# this function gets the all airports in the whole flight path
def legs(request):
    identifiers = request.GET.getlist('waypoint')
    print(identifiers)
    full_list = []
    for i in range(len(identifiers)):
        if (i + 1) != len(identifiers):
            weather_list = get_corridor_airports(identifiers[i], identifiers[i + 1])
            full_list += weather_list
    return render(request, 'clearskies_app/data.html', {'full_list': full_list})


def get_data(AI):
    beg_url = 'https://www.aviationweather.gov/metar/data?ids='
    end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'
    url = beg_url + AI + end_url
    res = requests.get(url)
    text = res.text
    find_beg = "<!-- Data starts here -->"
    find_end = "<br /><hr"
    beg_position_of_data = text.find(find_beg) + 25
    end_position_of_data = text.find(find_end)
    if "No METAR found" in text[beg_position_of_data:end_position_of_data]:
        return None
        # print("\n\n\n**********   GOT WEATHER   *************")
        # print(text[beg_position_of_data:end_position_of_data])
    return text[beg_position_of_data:end_position_of_data]


# Delete this when done testing
def coord(request):
    if request.method == "POST":
        temp = Airfield.objects.get(identifier=request.POST['airport'])
        testLAT = temp.latitude
        testLON = temp.longitude
    else:
        testLAT = ''
        testLON = ''
    context = { 'testLAT': testLAT, 'testLON': testLON }
    return render(request, 'clearskies_app/get_coord.html', context)
