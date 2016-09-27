# -*- coding: utf-8 -*-
from django import forms

class AttendForm(forms.Form):
    # TODO: Define form fields here
    display_name = forms.CharField(
        #label=_('姓名'),
        max_length=30,
        )
    department = forms.CharField(
        #label=_('部门'),
        max_length=30,
        )
    phonenumber = forms.CharField(
        #label=_('电话'),
        max_length=30,
        )
