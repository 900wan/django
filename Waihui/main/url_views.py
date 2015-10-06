 # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
# from django import forms
# from login.models import User
from main.act import act_signup
# from main.act import act_jisuan
from main.act import act_addlanguage
from main.act import act_showuser
from main.act import act_showindividual
from main.act import act_addtopic
from main.act import act_login
from main.act import act_htmllogin
from main.forms import LoginForm
from main.forms import SignupForm


# from main.act import 
def url_homepage(request):
    user_language = 'en'
    translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    tstr=_(u'Our hompage heading')
    return render(request, "main/home.html", {'heading':tstr})

def url_index(request,fuckset):
    boy = int(fuckset)
    # return render(request, 'pass', )
    # ace = act_jisuan(boy)
    # return HttpResponse(ace)

def url_signup(request):
    '''用户通过浏览器将表单内容post到/signup/post后来到这里'''
    if request.method == 'POST':
        act_signup(username, password, email, )
    # uf = SignupForm(request.POST)
    # act_signup()

def url_login(request):
    uf = LoginForm(request.POST)
    msg = request.method+' hehe '+str(uf.is_valid())
    if request.method == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "main/right.html", {'username':username})
                else:
                    return render(request, "main/isnotactive.html", {'username':username})
            else:
                return render(request, "main/wrong.html", {'username':username})
        else:
            return render(request, "main/login.html", {'uf':uf, 'msg':msg})
        # elif uf.is_valid():
        #     name=uf.cleaned_data['name']
        #     return render(request, 'main.test_result.html',{'uf':uf})
    else:
        return render(request, "main/login.html", {'uf':uf, 'msg':msg})

def url_tc(request, offset_id):
    return HttpResponse(offset_id)

def url_tutor(request, offset_id):
    '''For show tutor home page'''
    id = int(offset_id)
    act = act_showindividual(id, 'provider')
    return HttpResponse(act.status)

def url_order(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'order')
    return HttpResponse(act)

def url_lesson_prepare(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_summarize(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_rate(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_classroom(request):
    pass

def url_office(request):
    pass

def url_user(request,offset_id):
    id = int(offset_id)
    user = act_showindividual(id, 'user')
    usern = user.username
    email = user.email 
    password = user.password
    result = usern + email + password
    return HttpResponse(result)

def url_test_set(request,offset = 0 ):
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