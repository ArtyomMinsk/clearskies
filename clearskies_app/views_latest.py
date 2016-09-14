from django.shortcuts import render
from .models import Airfield
from numpy import arange
import requests

def home(request):
    return render(request, 'clearskies_app/index.html', context=None)


def TRW(request):
    if request.method == "POST":
        beg_url = 'https://www.aviationweather.gov/metar/data?ids='
        end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'
        print("############     running     ###############")
        places = Airfield.objects.all()
        count = 4000
        stop = 5000
        index = 0
        for each in places:
            if index > count and index < stop:
                temp = each.identifier
                tempp = list(temp)
                if tempp[0] != 'K':
                    AI = temp
                    print(AI, "   ", end="")
                    url = beg_url + AI + end_url
                    res = requests.get(url)
                    text = res.text
                    find_beg = "<!-- Data starts here -->"
                    find_end = "<br /><hr"
                    beg_position_of_data = text.find(find_beg) + 25
                    end_position_of_data = text.find(find_end)
                    if "No METAR found" not in text[beg_position_of_data:end_position_of_data]:
                        print("FOUND ONE !!!!", text[beg_position_of_data:end_position_of_data])
            index += 1
    return render(request, 'clearskies_app/plan.html', {})


def get_corridor_airports(request):
    if request.method == "POST":
        print("*********", request.POST)
        start = Airfield.objects.get(identifier=request.POST['start'])
        finish = Airfield.objects.get(identifier=request.POST['finish'])
        startLAT = start.latitude
        startLON = start.longitude
        finishLAT = finish.latitude
        finishLON = finish.longitude
        print("startLAT", startLAT, "startLON", startLON, "finishLAT", finishLAT, "finishLON", finishLON)
        print("*********")
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
        selected_airports = Airfield.objects.filter(latitude__gte=x1,
                                                    latitude__lte=x2,
                                                    longitude__gte=y1,
                                                    longitude__lte=y2)
        print("selected_airports: ", *selected_airports, sep='\n')
        print(len(selected_airports))
        lat_diff = abs(startLAT - finishLAT)
        lon_diff = abs(startLON - finishLON)
        if lon_diff > lat_diff:
            ratio = lat_diff / (lon_diff * 10)
            step_thru = "lon"
            if startLON < finishLON:
                increment = 0.1
                cushion = 0.4
            else:
                increment = -0.1
                cushion = -0.4
        else:
            ratio = lon_diff / (lat_diff * 10)
            step_thru = "lat"
            if startLAT < finishLAT:
                increment = 0.1
                cushion = 0.4
            else:
                increment = -0.1
                cushion = -0.4

        count = 0  # delete when testng done

        if step_thru == "lon":
            startP = startLON
            finishP = finishLON
        else:
            startP = startLAT
            finishP = finishLAT

        for i in arange(startP, finishP + cushion, increment):
            for each_airport in selected_airports:
                if step_thru == 'lon':
                    if each_airport.latitude <= startLAT + 0.4 and each_airport.latitude >= startLAT - 0.4 and each_airport.longitude <= i and each_airport.longitude >= i - 0.1:
                        count += 1
                        print("LON = ", each_airport.longitude, "    LAT = ", each_airport.latitude)
                        if startLAT > finishLAT:
                            startLAT -= ratio
                        else:
                            startLAT += ratio
                        print("SUCCESS!!!!!", each_airport, each_airport.latitude, each_airport.longitude, count)
                        # get_data(each_airport.identifier)

                elif step_thru == 'lat':
                    if each_airport.longitude <= startLON + 0.4 and each_airport.longitude >= startLON - 0.4 and each_airport.latitude <= i and each_airport.latitude >= i - 0.1:
                        count += 1
                        print("LON = ", each_airport.longitude, "    LAT = ", each_airport.latitude)
                        if startLON > finishLON:
                            startLON -= ratio
                        else:
                            startLON += ratio
                        print("SUCCESS!!!!!", each_airport, each_airport.latitude, each_airport.longitude, count)
                    # get_data(each_airport.identifier)
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

    return render(request, 'clearskies_app/test.html', {})


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
