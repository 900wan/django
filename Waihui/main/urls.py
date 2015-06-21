from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import url_views



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^time/plus/(\d{1,2})/$',url_views.url_index, name = "index"),
	url(r'^signup/$', url_views.url_signup_post, name = "signup_post"),
    url(r'^user/(\d{1,2})/$', url_views.url_user ,name = 'user' ),
    url(r'^test/$',url_views.url_test_set, name = "test"),
    url(r'^test/(\d{1,2})/$', url_views.url_test_set, name = 'test_setnum'),
)
