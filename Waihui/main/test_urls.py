from django.conf.urls import url
from main import test_views


urlpatterns = [
    url(r'^$', test_views.index, name='index'),
    url(r'^test/(\d{1,2})/$', test_views.url_test_set, name='test_setnum'),
    url(r'^testformff/$', test_views.url_modelformfk, name='urlmodelformfk'),
    url(r'^info/$', test_views.test_infolist, name='info'),
    url(r'^language/$', test_views.get_language, name='get_language'),
    url(r'^mytest/$', test_views.url_test, name="mytest"),
]

# test_patterns = [
#     url(r'$', test_views.url_test, ),
#     url(r'^testform/$', test_views.test_modelformfk, name='testmodelformfk'),
# ]
