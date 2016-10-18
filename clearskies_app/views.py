from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Airfield, METAR
from numpy import arange
import requests
# from django.views.decorators.cache import cache_page


def test(request):
    return render(request, 'clearskies_app/layout.html', context=None)


def get_corridor_airports(st, fin, width):
    airport_weather = []
    start = Airfield.objects.get(identifier=st)
    wx = get_data(start.identifier)
    if wx:
        airport_weather.append((start, METAR(wx)))
    finish = Airfield.objects.get(identifier=fin)
    start_lat = start.latitude
    start_lon = start.longitude
    finish_lat = finish.latitude
    finish_lon = finish.longitude

    if start_lat < finish_lat:
        x1 = start_lat
        x2 = finish_lat
    else:
        x2 = start_lat
        x1 = finish_lat
    if start_lon < finish_lon:
        y1 = start_lon
        y2 = finish_lon
    else:
        y2 = start_lon
        y1 = finish_lon
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
    lat_diff = abs(start_lat - finish_lat)
    lon_diff = abs(start_lon - finish_lon)
    if lon_diff > lat_diff:
        ratio = lat_diff / (lon_diff * 10)
        step_thru = "lon"
        if start_lon < finish_lon:
            increment = 0.1
            extend = 0.4
        else:
            increment = -0.1
            extend = -0.4
    else:
        ratio = lon_diff / (lat_diff * 10)
        step_thru = "lat"
        if start_lat < finish_lat:
            increment = 0.1
            extend = 0.4
        else:
            increment = -0.1
            extend = -0.4

    if step_thru == "lon":
        start_point = start_lon
        finish_point = finish_lon
    else:
        start_point = start_lat
        finish_point = finish_lat

    for i in arange(start_point, finish_point + extend, increment):
        if step_thru == 'lon':
            for each_airport in selected_airports:
                if each_airport.latitude <= start_lat + width and \
                    each_airport.latitude >= start_lat - width and \
                    each_airport.longitude <= i and \
                    each_airport.longitude >= i - 0.1:

                    wx = get_data(each_airport.identifier)
                    if wx:
                        airport_weather.append((each_airport, METAR(wx)))
            if start_lat > finish_lat:
                start_lat -= ratio
            else:
                start_lat += ratio

        elif step_thru == 'lat':
            for each_airport in selected_airports:
                if each_airport.longitude <= start_lon + width and \
                    each_airport.longitude >= start_lon - width and \
                    each_airport.latitude <= i and \
                    each_airport.latitude >= i - 0.1:

                    wx = get_data(each_airport.identifier)
                    if wx:
                        airport_weather.append((each_airport, METAR(wx)))
            if start_lon > finish_lon:
                start_lon -= ratio
            else:
                start_lon += ratio

    wx = get_data(finish.identifier)
    if wx:
        airport_weather.append((finish, METAR(wx)))
    dup = len(airport_weather) - 1
    for i in range(dup, 0, -1):
        if airport_weather[i] == airport_weather[i-1] or \
            airport_weather[i] == airport_weather[i-2]:
            airport_weather.pop(i)
    return airport_weather


# this function gets the all airports in the whole flight path
# @cache_page(60 * 15)
def legs(request):
    weather_stations = []
    identifiers = request.GET.getlist('waypoint')
    corr_width = request.GET.get('corridor_width')

    for i in range(len(identifiers)):
        if (i + 1) != len(identifiers):
            weather_list = get_corridor_airports(identifiers[i],
                                                 identifiers[i + 1],
                                                 float(corr_width))
        if i == 0:
            weather_stations += weather_list
        else:
            weather_stations += weather_list[1:]

    full_list = []
    airfield_ids = []
    for item in weather_stations:
        if item[0].identifier in airfield_ids:
            continue
        else:
            datapoint = {"identifier": item[0].identifier,
                         "name": item[0].name,
                         "city": item[0].city,
                         "state": item[0].state,
                         "latitude": item[0].latitude,
                         "longitude": item[0].longitude,
                         "ceiling": item[1].ceiling}
            full_list.append(datapoint)
            airfield_ids.append(item[0].identifier)
    return JsonResponse(full_list, safe=False)


def get_data(AI):
    beg_url = 'https://www.aviationweather.gov/metar/data?ids='
    end_url = '&format=raw&hours=0&taf=off&layout=on&date=0'
    url = beg_url + AI + end_url
    res = requests.get(url)
    text = res.text
    find_beg = "<!-- Data starts here -->"
    find_end = "<br /><hr"
    beg_position_of_data = text.find(find_beg) + 26
    end_position_of_data = text.find(find_end)
    if "No METAR found" in text[beg_position_of_data:end_position_of_data]:
        return None
    return text[beg_position_of_data:end_position_of_data]


def instant_plot(request):
    if request.method == "GET":
        temp = get_object_or_404(Airfield, identifier=request.GET['airportID'])
        airfield = {'latitude': temp.latitude,
                    'longitude': temp.longitude,
                    'name': temp.name,
                    'city': temp.city,
                    'state': temp.state,
                    'identifier': temp.identifier}
    else:
        airfield = {}
    return JsonResponse(airfield)


def all_airfields(request):
    airfields = Airfield.objects.all()
    identifiers = [airfield.identifier for airfield in airfields]
    return JsonResponse(identifiers, safe=False)
