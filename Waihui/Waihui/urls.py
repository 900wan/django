# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
import minutes
import easy_timezones
# from main import test_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace="main")),
    url(r'^p/', include('main.mvp_urls', namespace="mvp")),
    url(r'^minutes/', include('minutes.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^qr/(.+)$', minutes.views.generate_qrcode, name='qrcode'),
    url(r'^tz/', include('easy_timezones.urls')),
    # 尝试在Waihui的urls中添加test目录失效
    # url(r'^test/', test_urls),
    ]
