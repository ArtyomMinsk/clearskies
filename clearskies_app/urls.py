from django.conf.urls import url
from . import views

app_name = 'clearskies_app'
urlpatterns = [
    url(r'^Tindex/$', views.Tindex, name="Tindex"),
    url(r'^get_coord/$', views.coord, name="coord"),
    url(r'^plan/$', views.plan, name="plan"),
    url(r'^test/$', views.legs, name="legs"),
    url(r'', views.home, name="home"),
]
