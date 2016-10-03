 # -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cStringIO import StringIO
from minutes.models import *
from minutes.forms import *

def act_signinmeeting(display_name, department, phonenumber):
	profile = Profile(
		display_name=display_name,
		department=department,
		phonenumber=phonenumber,
		)
	profile.save()
	result = "OK, " + unicode(display_name) + _(u", 您已经成功签到，收藏该地址获取会议纪要")
	return result