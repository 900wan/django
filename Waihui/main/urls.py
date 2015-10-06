from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import url_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', url_views.url_homepage, name ="home_page"),
    url(r'^signup/$', url_views.url_signup, name = "signup"), 
    url(r'^login/$', url_views.url_login, name = "login"), 
    url(r'^user/(\d{1,2})/$', url_views.url_user ,name = 'user' ), 
    url(r'^tc/(\w*)/$', url_views.url_tc, name = 'topic_category'),
    url(r'^show/(\d{1,2})/$', url_views.url_tutor, name = 'show'),
    url(r'^time/plus/(\d{1,2})/$', url_views.url_index, name = "index"),
    url(r'^test/(\d{1,2})/$', url_views.url_test_set, name = 'test_setnum'),

)
