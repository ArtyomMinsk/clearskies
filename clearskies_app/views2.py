from django.shortcuts import render
from .models import Airfield
from numpy import arange
import requests

def home(request):
    return render(request, 'clearskies_app/index.html', context=None)


def cloud_bases_report(request):
    pass
    # print the list of
    # DEF  get coords of start and finish from DB
    # DEF  calc the rectangle
    # DEF  get all the stations within the LAT LON rectangle









def get_corridor_airports(request):
    if request.method == "POST":
        print("*********", request.POST)
        start = Airfield.objects.get(identifier=request.POST['start'])
        finish = Airfield.objects.get(identifier=request.POST['finish'])
        startLAT = start.latitude
        print("startLAT", startLAT, type(startLAT))
        startLON = start.longitude
        finishLAT = finish.latitude
        finishLON = finish.longitude
        print("*********")
        selected_airports = Airfield.objects.filter(latitude__gte=finishLAT, latitude__lte=startLAT, longitude__gte=startLON, longitude__lte=finishLON)
        print("selected_airports: ", *selected_airports, sep='\n')
        print(len(selected_airports))
        lat_diff = abs(startLAT - finishLAT)
        lon_diff = abs(startLON - finishLON)
        if lon_diff > lat_diff:
            ratio = lat_diff / (lon_diff * 10)
            # print("ratio", ratio)
            count = 0

            for i in arange(startLON, finishLON, 0.1):
                lon = i
                for each in selected_airports:
                    strippedLAT = each.latitude
                    strippedLON = each.longitude
                    if strippedLAT <= startLAT + 0.4 and strippedLAT >= startLAT - 0.4 and strippedLON <= lon and strippedLON >= lon - 0.1:
                        count += 1
                        print("SUCCESS!!!!!", each, each.latitude, each.longitude, count)
                        get_data(each.identifier)
                    # x1 -= ratio
                # else:
                    # print("outside the area", x1, lon)
                startLAT -= ratio
        #
        # context = {'startLAT': startLAT,
        #            'startLON': startLON,
        #            'finishLAT': finishLAT,
        #            'finishLON': finishLON
        #     }
    else:
        print("IT IS NOT POST REQUEST!!!!!!!!!!!")
        start = ''
        finish = ''

    return render(request, 'clearskies_app/plan.html', {})


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
    if "No METAR found" not in text[beg_position_of_data:end_position_of_data]:
        print("\n\n\n**********   GOT WEATHER   *************")
        print(text[beg_position_of_data:end_position_of_data])


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
