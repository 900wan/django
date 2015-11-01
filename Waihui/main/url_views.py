 # -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.utils import translation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
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
from main.act import act_getlanguage
from main.act import act_addsku
from main.act import act_addrts
from main.act import act_addplan
from main.act import act_showsku

from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import Sku
from main.models import ReplyToSku
from main.models import Plan

from main.forms import LoginForm
from main.forms import SignupForm
from main.forms import AddSkuForm
from main.forms import AddRTSForm
from main.forms import AddPlanForm

def url_homepage(request):
    language = act_getlanguage(request)
    user_language = language
    translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    tstr = _(u'Our hompage heading')
    return render(request, "main/home.html", {'heading':tstr})

def url_index(request,fuckset):
    boy = int(fuckset)
    # return render(request, 'pass', )
    # ace = act_jisuan(boy)
    # return HttpResponse(ace)

def url_signup(request):
    '''用户通过浏览器将表单内容post到/signup/post后来到这里'''
    uf = SignupForm(request.POST)
    language = act_getlanguage(request)
    msg = request.method + language
    if request.method == 'POST':
        if uf.is_valid():
            nickname = uf.cleaned_data['nickname']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            result = act_signup(password=password, nickname=nickname, email=email,
                http_language=language)
            msg = result + language
    return render(request, "main/signup.html", {'form':uf, 'msg':msg})
    # act_signup()

def url_login(request):
    uf = LoginForm(request.POST)
    msg = ''
    next = ''
    if request.GET:  
       next = request.GET['next']
    if request.method == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next == '':
                        return render(request, "main/right.html", {'username':username})
                    else:
                        return HttpResponseRedirect(next)
                else:
                    msg = _(u'Login failed, user is not active.')
                    return render(request, "main/login.html", {'uf':uf, 'msg':msg, 'next':next})
            else:
                msg = _(u'Guess what? Login failed.')
                return render(request, "main/login.html", {'uf':uf, 'msg':msg, 'next':next})
        else:
            msg = _(u'form not valid')
            return render(request, "main/login.html", {'uf':uf, 'msg':msg})
        # elif uf.is_valid():
        #     name=uf.cleaned_data['name']
        #     return render(request, 'main.test_result.html',{'uf':uf})
    else:
        return render(request, "main/login.html", {'uf':uf, 'msg':msg, 'next':next})

# @login_required
def url_logout(request):
    logout(request)
    return HttpResponse("logouted")

def url_tc(request, offset_id):
    return HttpResponse(offset_id)

def url_tutor(request, offset_id):
    '''For show tutor home page'''
    id = int(offset_id)
    act = act_showindividual(id, 'provider')
    return HttpResponse(act.status)

@login_required
def url_addsku(request):
    '''make a sku for order, One order can have many skus'''
    current_user=request.user
    skus = Sku.objects.all()
    uf = AddSkuForm(request.POST)
    msg = request.method+", user: ["+str(current_user.username)+"], user's buyer: ["+str(current_user.buyer)+"]"
    if request.method == 'POST':
        if uf.is_valid():
            provider = uf.cleaned_data['provider']
            topic = uf.cleaned_data['topic']
            start_time = uf.cleaned_data['start_time']
            end_time = uf.cleaned_data['end_time']
            result = act_addsku(provider=provider, topic=topic, start_time=start_time, end_time=end_time, buyer=current_user.buyer)
            msg = result
    return render(request, "main/addsku.html", {'uf':uf, 'msg':msg, 'heading':"add sku", 'skus':skus})
    # teachers = Provider.objects.all()
    # topics = Topic.objects.all()
    # 
    # return render(request, "main/addsku.html", {'teacher_list':teachers, 'topic_list':topics,})
    
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

def url_replytosku(request):
    '''handling the replys to sku,'''
    current_user = request.user
    rtss = ReplyToSku.objects.all()
    uf = AddRTSForm(request.POST)
    msg = request.method
    if request.method == 'POST':
        if uf.is_valid():
            sku = uf.cleaned_data['sku']
            content = uf.cleaned_data['content']
            replyto = uf.cleaned_data['reply_to']
            if current_user.provider == sku.provider:
                type = 1    
            else:
                type = 0
            result = act_addrts(user=current_user, type=type, content=content, reply_to=replyto,)
            msg = str(current_user)+", "+str(sku.provider)+", "+result
    return render(request, "main/addrts.html", {'uf':uf, 'msg':msg, 'heading':"Reply to Sku", 'rtss':rtss})

def url_addplan(request):
    current_user = request.user
    plans = Plan.objects.all()
    uf = AddPlanForm(request.POST)
    msg = request.method
    if request.method == 'POST':
        if uf.is_valid():
            sku = uf.cleaned_data['sku']
            topic = uf.cleaned_data['topic']
            status = uf.cleaned_data['status']
            content = uf.cleaned_data['content']
            assignment = uf.cleaned_data['assignment']
            slides = uf.cleaned_data['slides']
            materiallinks = uf.cleaned_data['materiallinks']
            materialhtmls = uf.cleaned_data['materialhtmls']
            voc = uf.cleaned_data['voc']
            result = act_addplan(sku=sku, topic=topic, status=status, content=content, 
                assignment=assignment, slides=slides, materialhtmls=materialhtmls, materiallinks=materiallinks, voc=voc)
            msg = result
    return render(request, "main/addplan.html", {'uf':uf, 'msg':msg, 'heading':"Add a plan on SKU", 'plans':plans})

def url_showsku(request, sku_id):
    id = int(sku_id)
    sku_id = id
    result = act_showsku(sku_id)
    msg = str(result) + ", " + str(result.topic)
    return render(request, "main/showsku.html", {'heading':"There is all SKUs", 'msg':msg})