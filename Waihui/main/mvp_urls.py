from django.conf.urls import url
from main import mvp_views


urlpatterns = [
    url(r'^$', mvp_views.home, name='home'),
]
