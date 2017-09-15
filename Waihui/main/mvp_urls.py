from django.conf.urls import url
from main import mvp_views


urlpatterns = [
    url(r'^$', mvp_views.home, name='home'),
    url(r'^dashboard/$', mvp_views.dashboard, name='dashboard'),

]

