from django.conf.urls import url
from . import views

app_name = 'clearskies_app'
urlpatterns = [
    url(r'^get_coord/$', views.get_coord, name="coord"),
    url(r'^plan/$', views.get_corridor_airports, name="plan"),
    url(r'^Tindex/$', views.Tindex, name="Tindex"),
    url(r'', views.home, name="home"),

]
