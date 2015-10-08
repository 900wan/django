# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from main import test_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace="main")),
    # 尝试在Waihui的urls中添加test目录失效
    # url(r'^test/', test_urls),
    )
