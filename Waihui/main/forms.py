# -*- coding: utf-8 -*-
from django import forms

class SignupForms(forms.Form):
    username = forms.CharField(
      # label=_('姓名'),
      max_length= 30,
    )

    # email = forms.EmailField(label=_('Email'),)

    password = forms.CharField(
      # label=_('password'),
      widget=forms.PasswordInput(),
    )

    password_2 = forms.CharField(
      # label=_('passowrd_confirmed'),
      widget=forms.PasswordInput(),
    )

    def clean_password_2(self):
      password = self.cleaned_data.get("password")
      password_2 = self.cleaned_data.get("password_2")
      if password and password_2 and password != password_2:
        raise forms.ValidationError(_('password confirm failed'))
      return password_2

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())