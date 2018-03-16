# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from django.utils import translation, timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from urllib import unquote

from main.test_act import *
from main.act import *
from main.models import *

from main.forms import TestModelformFKForm

def test_infolist(request):
    info = act_getinfo(request)
    heading = _(u'Provider list')
    provider = get_object_or_404(Provider, id=1)
    infolist = Provider.objects.all()
    result = act_pay_provider(provider)
    item = result['error']
    # item = act_provider_activity(provider)
    return render(request, "test/info.html", locals())

def url_test(request):
    return get_language(request)

def index(request):
    a = 'this is a test page'
    amount = 100
    offset = 10
    return render(request, 'test/test.html', locals())

def test_home(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)

def get_language(request):
    i = request.META.get('HTTP_ACCEPT_LANGUAGE')

    return render(request, 'test/test.html', {'lans':i})

def url_test_set(request, offset=0):
    ''''''
    set = int(offset)
    return render(request, 'test/test_form.html', locals())


def test_signup(set):
    if set == 0:
        b = act_signup(
        email="swee@msn.com",
        password="123",
        nickname="Bob",
        gender="1",
        mother_tongue_id=1,
        time_zone='America/Chicago')
    else:
        b=act_signup(
        email=str(set)+"swee@msn.com",
        password="123",
        nickname="Bob",
        gender="1",
        mother_tongue_id=1,
        time_zone='America/Chicago')
    return b

def test_addlanguage(set):
    if set == 0:
        result = act_addlanguage(
        english_name=str(set) + "english",
        chinese_name=str(set) + "英语",
        local_name=str(set) + "英语")
    else:
        result = act_addlanguage(
        english_name="english",
        chinese_name="英语",
        local_name="英语")
    return result


def test_addtopic(set):
    if set == 0:
        result = act_addtopic(
            name='支付宝',
            category='')

def test_modelformfk(request):
    ''''''
    info = act_getinfo(request)
    heading = "Test Modelformfk"
    if request.method == "POST":
        uf = TestModelformFKForm(request)
        uf.save(commit=False)
    else:
        uf = TestModelformFKForm()
    return render(request, "main/test_form.html", locals())



def url_test(request):
    info = act_getinfo(request)
    infos = ds_getanoti(Notification.objects.get(id=68))
    typeofinfos = type(info)
    typeofnotis = type(Notification.objects.get(id=68))
    return render(request, "main/mytest.html", locals())

def url_idtest(request, set_id):
    result = Test_skufunction(set_id)
    return render(request, "main/mytest", {'result':result})

def url_modelformfk(request):
    ''''''
    info = act_getinfo(request)
    heading = "Test Modelformfk"
    if request.method == "POST":
        uf = TestModelformFKForm(request.POST)
        if uf.is_valid():
            new_uf = uf.save(commit=False)
            sku = get_object_or_404(Sku, id=227)
            topic = sku.topic
            new_uf.sku = sku
            new_uf.topic = topic
            new_uf.save()
    else:
        uf = TestModelformFKForm()
    return render(request, "main/test_form.html", locals())

@login_required
def url_alipay_webtrade_test(request, amount):
    '''alipay webpage payment test'''
    info = act_getinfo(request)
    heading = _(u'AliPay trade_page_pay test')
    subject = _(u'Recharge moneny ') + str(amount)
    order_string = act_alipay_trade_page(subject, amount)
    alipayurl = "https://openapi.alipaydev.com/gateway.do?"
    alipayurlget = str(alipayurl) + str(order_string)
    decoderaw = unquote(order_string)

    splitraw = decoderaw.split('&')
    jsonraw = json.dumps(str(decoderaw))
    strsplitraw = str(splitraw)

    timenow = str(timezone.now())
    return render(request, "main/alipay_webtrade_test.html", locals())

@login_required
def url_alipay_webtrade_return(request):
    '''Alipay webpage payment return'''
    info = act_getinfo(request)
    heading = _(u'Alipay Return Page')
    if request.GET:
        data = request
        total_amount = request.total_amount
        timestamp = request.timestamp
        sign = request.sign
        trade_no = request.trade_no
        sign_type = request.sign_type
        auth_app_id = request.auth_app_id
        charset = request.charset
        seller_id = request.seller_id
        method = request.method
        app_id = request.app_id
        out_trade_no = request.out_trade_no
        version = request.version
    return render(request, "main/alipay_webtrade_return.html", locals())


