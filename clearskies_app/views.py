from django.shortcuts import render
from .models import Airfield


def home(request):
    return render(request, 'clearskies_app/index.html', context=None)

def cloud_bases_report(request):
    # print the list of
    #DEF  get coords of start and finish from DB
    #DEF  calc the rectangle
    #DEF  get all the stations within the LAT LON rectangle
