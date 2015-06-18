# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def ds_checkrequest_form():
    if request.method == 'POST':
        return HttpResponse("good condition")
    else :
        ds_return_check
    return ds_return_check    

def ds_return_check():
    return HttpResponse('this is used by return_check')

def act_signup():
    ds_checkrequest_form

def url_signup_post(request):
# "用户通过浏览器将表单内容post到/signup/post后来到这里"
    act_signup
    

def url_index(request):
    # return render(request, 'pass', )
    return HttpResponse('Question')