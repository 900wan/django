# -*- coding: utf-8 -*-
import pytz, json, datetime 
from alipay import AliPay, ISVAliPay
from django.utils import translation, timezone
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from main.ds import *
from main.models import *
from main.act import *

# def act_addplan(sku, topic, status, content, assignment, slides, roomlink, materiallinks, materialhtml, voc, copy_from, sumy, plan=None):
#     '''if import a plan, it will change the plan, if not, then add one'''
#     if plan:
#         plan.status = status
#         plan.content = content
#         plan.assignment = assignment
#         plan.slides = slides
#         plan.roomlink = roomlink
#         plan.materialhtml = materialhtml
#         plan.materiallinks = materiallinks
#         plan.voc = voc
#         plan.copy_from = copy_from
#         plan.sumy = sumy
#         result = "OK, Plan: " + sku.provider.name + " & " + topic.name + " modified!"
#         ds_noti_tobuyer_planmodified(plan)
#     else:
#         plan = Plan(
#             sku=sku,
#             topic=topic,
#             status=status,
#             content=content,
#             assignment=assignment,
#             slides=slides,
#             roomlink=roomlink,
#             materialhtml=materialhtml,
#             materiallinks=materiallinks,
#             voc=voc,
#             copy_from=copy_from,
#             sumy=sumy,
#             )
#         plan.save()
#         sku.status = 5
#         sku.save()
#         result = "OK, Plan: " + sku.provider.name + " & " + topic.name + " added!"
#         ds_noti_tobuyer_newplan(plan)
#     return result

def test_alipay_trade_page():
    subject = u"测试订单".encode("utf8")
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="20161112",
        total_amount=0.01,
        subject=subject,
        return_url="https://example.com",
        notify_url="https://example.com/notify" # 可选, 不填则使用默认notify url
        )
    return order_string

def act_pay_provider(provider, date=timezone.now()):
    '''for paying the provider, set a date, and sum the total salary.'''
    result = {}
    skus = provider.sku_set.filter(Q(created__lte=date)&Q(status=9)&Q(providerpayoff=None))
    amount = 0
    result['error'] = ''
    if skus.count() != 0:
        amount = skus.count()*act_provider_activity(provider)
        newpp = ProviderPayoff(provider=provider, amount=amount)
        newpp.save()
        for sku in skus:
            newpp.skus.add(sku)
    else:
        result['error'] = str('No available SKU')
    result['amount'] = amount if amount else False
    return result
