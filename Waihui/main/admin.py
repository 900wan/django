# -*- coding: utf-8 -*-
from django.contrib import admin
from main.models import *
class ProviderInfo(admin.ModelAdmin):
    # Provider.last_activity.editable = True
    list_display = ('__unicode__', 'id', 'user', 'name', 'status', 'fee_rate')

# @admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    '''Admin View for Log'''

    list_display = ('__unicode__', 'created', 'id', 'user', 'client', 'action', 'activity_action', 'activity_change')

    list_filter = ('action',)
    search_fields = ('activity_change', )
    date_hierarchy = 'created'
    # # inlines = [
    # #     Inline,
    # # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # ordering = ('',)


# Register your models here.
admin.site.register(Provider, ProviderInfo)
admin.site.register(Buyer)
admin.site.register(Language)
admin.site.register(Topic)
admin.site.register(Sku)
admin.site.register(TopicCategory)
admin.site.register(Log, LogAdmin)
admin.site.register(ActLog)
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
