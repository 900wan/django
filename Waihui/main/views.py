# -*- coding: utf-8 -*-
 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse


# Create your views here.
def ds_checkrequest_form():
    if request.method == 'POST':
        return "required.method = POST"
    else :
        return "else return"
    return 

def ds_return_check():
    return HttpResponse('this is used by return_check')

def act_signup():
    return ds_checkrequest_form()

def act_return_check():
	return 'Hi there'

def url_signup_post(request):
# "用户通过浏览器将表单内容post到/signup/post后来到这里"
    # word = act_return_check()
    # word = act_signup()
    if request.method == 'POST':
        return HttpResponse ("required.method = POST")
    else :
        return HttpResponse ("else return")
    return HttpResponse (word)
    

def url_index(request):
    # return render(request, 'pass', )
    return HttpResponse('Question')

