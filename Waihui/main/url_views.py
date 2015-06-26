# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from main.act import act_signup
# from main.act import act_jisuan
from main.act import act_addlanguage
from main.act import act_showuser
from main.act import act_showindividual

# from main.act import 

def url_signup_post(request):
    '''用户通过浏览器将表单内容post到/signup/post后来到这里'''
    # word = act_return_check()
    # word = act_signup()
    # if request.method == 'POST':
    #     act_signup(username, password, email, )
    pass

def url_index(request,fuckset):
    boy = int(fuckset)
    # return render(request, 'pass', )
    # ace = act_jisuan(boy)
    # return HttpResponse(ace)

def url_homepage(request):
    '''首页'''
    return HttpResponse("Hi! 900wan team give you a warm welcome!")

def url_login(request):
    pass

def url_tc(request):
    pass

def url_tutor(request, offset_id):
    '''For show tutor home page'''
    provider_id = int(offset_id)
    # c = 0 为 user，1为buyer，2为provider
    act = act_showindividual(provider_id, c=2)
    return HttpResponse(act.name)

def url_order(request, offset_id):
    order_id = int(offset_id)
    act = act_showorder(order_id)
    return HttpResponse(act)

def url_lesson_prepare(request, offset_id):
    sku_id = int(offset_id)
    act = act_showsku(sku_id)
    return HttpResponse(act)

def url_lesson_summarize(request, offset_id):
    sku_id = int(offset_id)
    act = act_showsku(sku_id)
    return HttpResponse(act)

def url_lesson_rate(request, offset_id):
    sku_id = int(offset_id)
    act = act_showsku(sku_id)
    return HttpResponse(act)

def url_classroom(request):
    pass

def url_office(request):
    pass

def url_user(request,offset):
    id = int(offset)
    user = act_showuser(id)
    username = user.username
    email = user.email 
    password = user.password
    result = username + email + password
    return HttpResponse(result)

def url_test_set(request,offset = 0 ):
    set = int(offset)
    act = test_signup(set)
    return HttpResponse(act)













def test_signup(set):
    if set == 0:
        b = act_signup(
        email= "swee@msn.com",
        password = "123",
        nickname = "Bob",
        gender = "1",
        mother_tongue_id = 1,
        time_zone = 'America/Chicago')
    else:
        b = act_signup(
        email= str(set) + "swee@msn.com",
        password = "123",
        nickname = "Bob",
        gender = "1",
        mother_tongue_id = 1,
        time_zone = 'America/Chicago')
    return b

def test_addlanguage(set):
    if set == 0:
        result = act_addlanguage(
        english_name = str(set) + "english",
        chinese_name = str(set) + "英语",
        local_name = str(set) + "英语")
    else:
        result = act_addlanguage(
        english_name = "english",
        chinese_name = "英语",
        local_name = "英语")
    return result