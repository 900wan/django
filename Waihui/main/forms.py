# -*- coding: utf-8 -*-
from django import forms
from main.models import Provider
from main.models import Topic 
from main.models import Sku
from main.models import ReplyToSku
from main.models import Plan
from main.models import Order

class SignupForm(forms.Form):
    nickname = forms.CharField(
      # label=_('姓名'),
      max_length=30,
    )

    email = forms.EmailField(label='Email',)

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
        raise forms.ValidationError('password confirm failed')
      return password_2

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

class AddSkuForm(forms.Form):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

class AddRTSForm(forms.Form):
    # sku = forms.ModelChoiceField(queryset=Sku.objects.all())
    content = forms.CharField(widget=forms.Textarea())
    # reply_to = forms.ModelChoiceField(queryset=ReplyToSku.objects.all(), required=False)
    reply_to = forms.ModelChoiceField(queryset=None, required=False)

class AddPlanForm(forms.Form):
    # sku = forms.ModelChoiceField(queryset=Sku.objects.all())
    # topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    status = forms.IntegerField()
    content = forms.CharField(widget=forms.Textarea())
    assignment = forms.CharField(widget=forms.Textarea(), required=False)
    slides = forms.CharField(widget=forms.Textarea(), required=False)
    roomlink = forms.URLField(required=False)
    materiallinks = forms.CharField(widget=forms.Textarea(), required=False)
    materialhtml = forms.CharField(widget=forms.Textarea(), required=False)
    voc = forms.CharField(widget=forms.Textarea(), required=False)
    copy_from = forms.ModelChoiceField(queryset=Plan.objects.all(), required=False)
    sumy = forms.CharField(widget=forms.Textarea(), required=False)

    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('skus',)
    
