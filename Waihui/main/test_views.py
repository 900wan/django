# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.http import HttpResponse

def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)

def get_language(request):
    i = request.META
    return i

def url_test_set(request, offset=0):
    set = int(offset)
    act = test_signup(set)
    return HttpResponse(act)


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