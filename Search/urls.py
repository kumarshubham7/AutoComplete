from django.conf.urls import url
from . import views
app_name = "search_keyword"
urlpatterns = [
    url(r'^addData/$', views.settings, name="settings"),
    url(r'^', views.search, name="search"),

]
