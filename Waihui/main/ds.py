# -*- coding: utf-8 -*-
from django.utils import translation, timezone
from django.core.urlresolvers import reverse
from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import TopicCategory
from main.models import Sku
from main.models import Plan
from main.models import Order
from main.models import Wallet
from main.models import ReplyToSku
from main.models import ReviewToProvider
from main.models import ReviewToBuyer
from main.models import Log
from main.models import Notification
import datetime

def ds_showtopic(id=0, bywhat=0):
    if bywhat == 0:
        topic = Topic.objects.get(id=id)
    elif id == 0:
        topic = Topic.objects.order_by('bywhat')
    elif bywhat == 0 & id == 0:
        topic = "error"
    return topic

def ds_addlog(source, type, user, character):
    user=User.objects.get(id=user)
    log = Log(source=source,
        type=type,
        user=user,
        character=character)
    log.save()
    return "OK!" + "from " + log.source + "log.user" + " logged in"

def ds_getanoti(noti):
    if noti.noti == 0:
        content = u"Your tutor <strong>%s</strong> left a comment:<br/> <i>%s</i><br>-- from <i>Topic: %s</i>" % (noti.reply.user.provider.name, noti.reply.content, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 10:
        content = u"Your student <strong>%s</strong> left a comment:<br/> <i>%s</i><br>-- from <i>Topic: %s</i>" % (noti.reply.user.buyer.nickname, noti.reply.content, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 3:
        content = u"the <strong>%s</strong>'s \" <strong>%s</strong> \" class will begin in 30 mins" % (noti.sku.provider.name, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    elif noti.noti == 6:
        content = u"Your teacher <strong>%s</strong> canceled your course:<br/>-- <i>Topic: %s</i>" % (noti.user.provider.name, noti.sku.topic.name)
        link = reverse('main:showsku', args=[noti.sku.id])
    anoti={
    'id': noti.id,
    'read' : noti.read,
    'content' : content,
    'link' : link,
    }
    return anoti

def ds_noti_newreply(reply, user, type):
    noti = 0 if type == 1 else 10
    notification = Notification(user=user,
        reply=reply, sku=reply.sku, open_time = timezone.now(), close_time = timezone.now() + datetime.timedelta(weeks=100), noti=noti)
    notification.save()
    return True

# def ds_noti_newcancel(sku, user, type):
#     noti = 6 if type == 1 else 9
#     notification = Notification(user=user,
#         sku=sku, open_time = timezone.now(),
#         close_time = timezone.now() + datetime.timedelta(weeks=100),
#         noti=noti)
#     notification.save()
#     return True

def ds_get_order_cny_price(skus):
    SKU_CNY_PRICE = 90.00
    cny_price = len(skus) * SKU_CNY_PRICE
    return cny_price

def ds_noti_noprovider(sku):
    """给学生发一个 noti 说完蛋了课不上了"""
    for buyer in sku.buyer.all():
        notification = Notification(user=buyer.user ,sku=sku, noti=6, open_time = timezone.now(), close_time = timezone.now() + datetime.timedelta(weeks=100))
        notification.save()
    return True

def ds_noti_buyercancel(sku, buyer):
    pass