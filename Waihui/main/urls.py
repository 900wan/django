from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import url_views
from main import test_views

test_patterns = patterns('',
                         url(r'$', test_views.url_test, ),
                         url(r'language/$', test_views.get_language, name='get_language'))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       url(r'^test/$', include(test_patterns)),
                        # url(r'^test/$', url_views.url_test, name='url_test'),
                        url(r'^$', url_views.url_homepage, name="home"),
                        url(r'^signup/$', url_views.url_signup, name="signup"), 
                        url(r'^login/$', url_views.url_login, name="login"), 
                        url(r'^logout/$', url_views.url_logout, name='logout'),
                        url(r'^user/(\d{1,2})/$', url_views.url_user, name='user'), 
                        url(r'^tc/(\w*)/$', url_views.url_tc, name='topic_category'),
                        url(r'^show/(\d{1,2})/$', url_views.url_tutor, name='tutor'),
                        # url(r'^time/plus/(\d{1,2})/$', url_views.url_index, name="index"),
                        url(r'^addsku/$', url_views.url_addsku, name='addsku'),
                        url(r'^sku/$', url_views.url_skulist, name='skulist'),
                        url(r'^sku/(\d{1,2})/$', url_views.url_showsku, name='showsku'),
                        url(r'^sku/(\d{1,2})/addplan/$', url_views.url_addplan, name='addplan'),
                        # url(r'^addplan/$', url_views.url_addplan, name='addplan'),
                        url(r'^sku/(\d{1,2})/reply/$', url_views.url_replytosku, name="replyrts"),
                        url(r'^mytest/$', url_views.url_test, name="mytest"),
                        url(r'^mytest/(\d{1,2})/$', url_views.url_idtest, name="idtest"),
                        # url(r'^reviews/$', url_views.url_reviews, name='reviews'),
    )
