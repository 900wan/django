from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$',views.url_index, name = "index"),
	url(r'^signup/$', views.url_signup_post, name = "signup_post"),
)
