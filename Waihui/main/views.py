# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
def ds_checkrequest_form():
    if request.method == 'POST':
        return "good condition"

def act_signup():
    ds_checkrequest_form

def url_signup_post(request):
# "用户通过浏览器将表单内容post到/signup/post后来到这里"
    act_signup
    ds_

def url_index():
    return "This is index."