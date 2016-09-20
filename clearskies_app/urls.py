from django.conf.urls import url
from . import views

app_name = 'clearskies_app'
urlpatterns = [
   url(r'^plan/$', views.home, name="plan"),
   url(r'^instant_plot/$', views.instant_plot, name="plot"),
   url(r'^fp/', views.legs, name="flightplan"),
   url(r'^airfields', views.all_airfields, name="airfields"),
]
