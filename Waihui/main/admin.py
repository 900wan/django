# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import *
class ProviderInfo(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'status', 'fee_rate')
    

# Register your models here.
admin.site.register(Provider, ProviderInfo)
admin.site.register(Buyer)
admin.site.register(Language)
admin.site.register(Topic)
admin.site.register(Sku)
admin.site.register(TopicCategory)
admin.site.register(Log)
admin.site.register(Wallet)
admin.site.register(ReplyToSku)
admin.site.register(Plan)
admin.site.register(Notification)
admin.site.register(Order)
admin.site.register(OrderType)
admin.site.register(ReviewToProvider)
admin.site.register(ReviewToBuyer)
admin.site.register(FeedbackQuestionnaireB2P)
admin.site.register(TestModelformFK)
admin.site.register(ProviderPayoff)
