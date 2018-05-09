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

def act_count_sku_earning(sku):
    '''Count provider sku earning right after a sku was finished
    if the interval between two sku is less than 7 days, 
    then the logrates will be count user recenly 7 days log information.
    else will count days log information between two sku 
    '''
    previous_skus = Sku.objects.filter(Q(provider=sku.provider)&Q(start_time__lte=sku.start_time)).order_by('-start_time')[:2:-1]
    previous_sku = previous_skus[0]
    interval_days = (previous_skus[1].start_time - previous_skus[0].start_time).days
    if interval_days < 7:
        logrates = act_user_activity(sku.provider.user, sku.start_time)
    else:
        logrates = act_user_activity(sku.provider.user, sku.start_time, interval_days)
    return logrates

def act_user_activity(user, set_date=timezone.now(), days=7):
    '''默认返回用户7天内的活跃度，
    ###目前只涉及教师，如非教师 不返回值。###
    希望包含是否每日登录，每周登录次数，
    据结算周期内每周登录频度，结算周期内可上课时长，结算周期内上课时长'''
    set_date = set_date.date()
    if user.provider.status != 0:
        from_date = set_date - datetime.timedelta(days=days)
        log_info = user.log_set.filter(Q(created__gte=from_date)&Q(created__lte=set_date))
        log_info = log_info.order_by('created').reverse()[::-1]    
        logrates = ds_lograte(set_date, log_info, days)
    
    return logrates

def act_wallet_trans(user, set_date=timezone.now(), forward_days=7):
    '''默认返回用户从现在到7天前的钱包转账情况，可定义开始时间，向前天数'''
    set_date = set_date.date()
    log_wallet = user.log_set.filter(Q())

def act_addlog_dailyacti(parameter_list):
    '''TODO:Try to make a def can handle all daily activity change
    '''
    pass

def add_addlog_provacti(parameter_list):
    '''TODO:Try to make a def handle all provider acti change
    by passing the sub def such as act_addlog_dailyacti'''
    pass

def act_addlog_schedule(user, last_schdule_weeknum, client=0):
    '''Add a log of adding a schedule'''
    addtional_content = "last_schdule_weeknum"
    addtional_value = last_schdule_weeknum
    log = ds_addlog(action=8,
        user=user,
        client=client,
        addtional_content=addtional_content,
        addtional_value=addtional_value)
    # check星期五24点前更新下周课表(+1)
    log = ds_log_addacti(log, 20)
    return log