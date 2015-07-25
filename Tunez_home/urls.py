from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/', views.searchrequest, name='searchrequest'),
    url(r'^download/', views.albumart, name='albumart'),
    url(r'^art/', views.artdownload, name='artdownload'),
]