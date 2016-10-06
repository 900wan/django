 # -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cStringIO import StringIO
from minutes.models import *
from minutes.forms import *
from minutes.acts import *
from minutes.statics import *
import urllib2
import json
import qrcode


def index(request):
    return HttpResponse("This is Javy Chen Minutes!")


def generate_qrcode(request, data):
    img = qrcode.make(data.replace("[q]","?"))
    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    response['Last-Modified'] = 'Sun, 10 Jul 2016 12:05:03 GMT'
    response['Cache-Control'] = 'max-age=31536000'
    return response


def entry_detail(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return render(request, "entry_detail.html", locals())


def qrcode_show(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    appid = APPID
    qr = "/qr/"
    return render(request, "qrcode_show.html", locals())

def qr_jumper(request, entry_id):
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APPID + "&redirect_uri=http://" + request.META['HTTP_HOST'] + "/minutes/"+ entry_id +"/wxsignin/&response_type=code&scope=snsapi_userinfo#wechat_redirect"
    testurl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=" + APPID + "&redirect_uri=http://" + request.META['HTTP_HOST'] + "/minutes/"+ entry_id +"/trys/&response_type=code&scope=snsapi_userinfo#wechat_redirect"
    return HttpResponseRedirect(testurl)


def easy_signin(request, entry_id, wx_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        uf = AttendForm(request.POST)
        if uf.is_valid():
            display_name = uf.cleaned_data['display_name']
            department = uf.cleaned_data['department']
            phonenumber = uf.cleaned_data['phonenumber']
            result = act_signinmeeting(display_name=display_name, department=department, phonenumber=phonenumber, entry=entry, wx_id=wx_id)
            return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
    else:
        uf = AttendForm()
        result = "请将参会信息填写完整"
    return render(request, "easy_signin.html", locals())

def wechat_signin(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    wx_id = act_wxqrget_wx_id(request)
    # wx_id = 'onlpmwit78qut1273l9jdx5LJgac'
    if Profile.objects.filter(wx_id=wx_id):
        profile = get_object_or_404(Profile, wx_id=wx_id)
        if profile.entry.filter(id=entry.id):
            return HttpResponse("already")
        profile.entry.add(entry)
        return HttpResponse("yes")
    else:
        if request.method == 'POST':
            uf = AttendForm(request.POST)
            if uf.is_valid():
                display_name = uf.cleaned_data['display_name']
                department = uf.cleaned_data['department']
                phonenumber = uf.cleaned_data['phonenumber']
                result = act_signinmeeting(display_name=display_name, department=department, phonenumber=phonenumber, entry=entry, wx_id=wx_id)
                return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
        else:
            uf = AttendForm()
            result = "请将参会信息填写完整"
    return render(request, "easy_signin.html", locals())

def trys(request, entry_id):
    wx_id = act_wxqrget_wx_id(request)
    # profile = Profile.objects.get(wx_id=wx_id)
    # entry = get_object_or_404(Entry, id=entry_id)
    # profile.entry.add(entry)
    return HttpResponse(wx_id)


