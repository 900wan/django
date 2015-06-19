# -*- coding: utf-8 -*-
class UserSignupForm(forms.Form):
    username = forms.CharField(
    	label=_('姓名'),
    	max_length= 30,
    )

   	email = forms.EmailField(label=_('Email'),)

   	password_1 = forms.CharField(
   		label=_('password'),
   		widget=forms,PasswordInput,
   	)

   	password_2 = forms.CharField(
   		label=_('passowrd_confirmed'),
   		widget=forms.PasswordInput,
   	)

   	def clean_password_2(self):
   		password_1 = self.cleaned_data.get("password_1")
   		password_2 = self.cleaned_data.get("password_2")
   		if password_1 and password_2 and password_1 != password_2:
   			raise form.ValidationError(_('password confirm failed'))
   		return password_2

class FORMNAME(forms.Form):
       # TODO: Define form fields here
          