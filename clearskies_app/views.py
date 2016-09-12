from django.shortcuts import render
from .models import Airfield


def home(request):
    return render(request, 'clearskies_app/index.html', context=None)


def cloud_bases_report(request):
    pass
    # print the list of
    # DEF  get coords of start and finish from DB
    # DEF  calc the rectangle
    # DEF  get all the stations within the LAT LON rectangle


def plan(request):
    if request.method == "POST":
        print(request.POST)
        start = Airfield.objects.get(identifier=request.POST['start'])
        finish = Airfield.objects.get(identifier=request.POST['finish'])
    else:
        start = ''
        finish = ''
    return render(request, 'clearskies_app/plan.html', {'start': start,
                                                        'finish': finish})
