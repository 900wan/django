 # -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from cStringIO import StringIO
from minutes.models import *
from minutes.forms import *
from minutes.acts import *
import qrcode


def index(request):
    return HttpResponse("This is Javy Chen Minutes!")


def generate_qrcode(request, data):
    img = qrcode.make(data)
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
    return render(request, "qrcode_show.html", locals())


def easy_signin(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        uf = AttendForm(request.POST)
        if uf.is_valid():
            display_name = uf.cleaned_data['display_name']
            department = uf.cleaned_data['department']
            phonenumber = uf.cleaned_data['phonenumber']
            result = act_signinmeeting(display_name=display_name, department=department, phonenumber=phonenumber, entry=entry)
            return HttpResponseRedirect(reverse('entry_detail', args=[entry_id]))
    else:
        uf = AttendForm()
        result = "请将参会信息填写完整"
    return render(request, "easy_signin.html", locals())

def wechat_signin(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'GET':
        code = request.GET['code']
    returncode = HttpResponseRedirect("https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxd78d86d0ebcc727b&secret=222b3622f6f6070eb408a244d9d142a7&code="+ str(code) +"&grant_type=authorization_code")
    return HttpResponse(returncode)