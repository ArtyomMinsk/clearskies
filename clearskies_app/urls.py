from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page

app_name = 'clearskies_app'
urlpatterns = [
   # url(r'^plan/$', cache_page(60 * 2)(views.home), name="plan"),
   url(r'^instant_plot/$', views.instant_plot, name="plot"),
   url(r'^fp/', views.legs, name="flightplan"),
   url(r'^airfields', views.all_airfields, name="airfields"),
   url(r'^test/$', views.test, name="plan"),
]
