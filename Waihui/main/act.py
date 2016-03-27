# -*- coding: utf-8 -*-
import pytz, json, datetime
from django.utils import translation, timezone
from django.core.urlresolvers import reverse
from django.db.models import Q
from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import TopicCategory
from main.models import Sku
from main.models import Plan
from main.models import Order
from main.models import OrderType
from main.models import Wallet
from main.models import ReplyToSku
from main.models import ReviewToProvider
from main.models import ReviewToBuyer
from main.models import Log
from main.models import Notification
from main.forms import OrderForm

from main.ds import ds_addlog
from main.ds import ds_getanoti
from main.ds import ds_noti_newreply
from main.ds import ds_get_order_cny_price
from main.ds import ds_noti_tobuyer_noprovider
from main.ds import ds_noti_toprovider_lostbuyer
from main.ds import ds_change_provider
from main.ds import ds_noti_toprovider_skubooked

from django.utils.translation import ugettext as _

MIN_CANCEL_TIME = datetime.timedelta(hours=8)
OK_CANCEL_TIME = datetime.timedelta(hours=12)
BEFORE_COURSE_TIME = datetime.timedelta(minutes=15)

def act_getlanguage(request):
    language = request.LANGUAGE_CODE
    # language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    return language

def act_signup(email, password, nickname, http_language, time_zone="Asia/Shanghai"):
    '''signup a user'''
    
    language = http_language
    try:
        ulanguage = Language.objects.get(english_name=language)
    except Language.DoesNotExist:
        ulanguage = Language(english_name=language)
        ulanguage.save()
    
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password)
    user.save()

    buyer = Buyer(
        user=user,
        nickname=nickname,
        # gender=gender,
        mother_tongue=ulanguage,
        time_zone=time_zone)
    buyer.save()

    provider = Provider(
        user=user,
        status=0,
        name=nickname)
    provider.save()

    wallet = Wallet(
        user=user)
    wallet.save()

    result = "OK!" + str(email) + "." + str(nickname) + "has added"
    # except:
    #     pass
    return result

def act_addlanguage(chinese_name, english_name, local_name):
    '''add a language'''
    language = Language(
        chinese_name=chinese_name,
        english_name=english_name,
        local_name=local_name,)
    language.save()
    result = "OK, Language:" + local_name + " added!"
    return result

def act_addtc(name, url):
    '''add a TopicCategory'''
    topiccategory = TopicCategory(
        name=name,
        url=url)
    topiccategory.save()
    result = "OK, Topic category:" + name + " added!"
    return result

def act_addtopic(name, topic_id, status, user_id):
    '''add a Topic'''
    topic = Topic(
        name=name,
        category=Topic.objects.get(id=topic_id),
        status=status,
        creator=User.objects.get(id=user_id))
    topic.save()
    result = "OK, Topic:" + name + " added!"
    return result

def act_addsku(provider, start_time, end_time, topic=None, buyer=None, status=0):
    '''it will add a Sku'''
    # provider = Provider.objects.get(id=provider_id)
    # topic = Topic.objects.get(id=topic_id)
    if start_time>=end_time:
        result = 'Opps, end_time must be later than start_time!'
    elif Sku.objects.filter(
        Q(provider=provider) & ~Q(status = 10), 
        Q(start_time__lte=start_time, end_time__gt=start_time) 
        | Q(start_time__lt=end_time, end_time__gte=end_time) 
        | Q(start_time__gt=start_time, end_time__lt=end_time)
        ):
        result = 'Opps, Time[%s] to [%s] is not available for %s!'  % (start_time, end_time, provider)
    else:
        sku = Sku(
            provider=provider,
            status=status,
            start_time=start_time,
            end_time=end_time,
            topic=topic,
            )
        sku.save()
        if buyer is not None:
            sku.buyer.add(buyer)
        result = "OK, Sku:" + provider.name + "'s " + str(start_time) + " added!"
    return result

def act_addplan(sku, topic, status, content, assignment, slides, roomlink, materiallinks, materialhtml, voc, copy_from, sumy):
    '''it will add a sku '''
    plan = Plan(
        sku=sku,
        topic=topic,
        status=status,
        content=content,
        assignment=assignment,
        slides=slides,
        roomlink=roomlink,
        materialhtml=materialhtml,
        materiallinks=materiallinks,
        voc=voc,
        copy_from=copy_from,
        sumy=sumy,
        )
    plan.save()
    result = "OK, Plan: " + sku.provider.name + " & " + topic.name + " added!"
    return result

def act_addrtp(provider_id, buyer_id, sku_id, questionnaire, score):
    '''it will add a ReviewToProvider'''
    provider = Provider.objects.get(id=provider_id)
    buyer = Buyer.objects.get(id=buyer_id)
    sku = Sku.objects.get(id=sku_id)
    rtp = ReviewToProvider(
        provider=provider,
        buyer=buyer,
        sku=sku,
        questionnaire=questionnaire,
        score=score)
    rtp.save()
    result = "OK, " + provider.name + "has leave a review on " + sku + "to " + Buyer.name
    return result

def act_addrtb(provider_id, buyer_id, sku_id):
    '''it will add a ReviewToBuyer'''
    provider = Provider.objects.get(id=provider_id)
    buyer = Buyer.objects.get(id=buyer_id)
    sku = Sku.objects.get(id=sku_id)
    rtb = ReviewToBuyer(
        provider=provider,
        buyer=buyer,
        sku=sku,
        )
    rtb.save()
    result = "OK, " + provider.name + "has leave a review to " + Buyer.name
    return result

def act_addrts(user, type, content, reply_to, sku):
    '''it will add a ReplyToSku'''
    rts = ReplyToSku(
        user=user,
        type=type,
        content=content,
        reply_to=reply_to,
        sku=sku,
        )
    rts.save()

    if rts.type == 1:
        for noti_buyer in sku.buyer.all():
            ds_noti_newreply(reply=rts, user=noti_buyer.user, type=1)
    elif rts.type == 0:
        ds_noti_newreply(reply=rts, user=sku.provider.user, type=0)
    

    result = "OK, " + user.username + " left a message of" + content
    return result

def act_updatewallet():
    pass

def act_showuser(id):
    '''it will show User information'''
    user = User.objects.get(id=id),
    return user

def act_showprovider(id):
    '''it will show Provider information'''
    provider = Provider.objects.get(id=id)
    return provider

def act_showbuyer(id):
    '''it will show Buyer information'''
    buyer = Buyer.objects.get(id=id)
    return buyer

def act_showorder(id):
    '''it will show Order information'''
    order = Sku.objects.get(id=id)
    return order

def act_showtopic(id):
    """this will show a topic"""
    topic = Topic.objects.get(id=id)
    return topic

def act_showtc(id):
    """it will show a topiccategory"""
    tc = TopicCategory.objects.get(id=id)
    return tc

def act_signtopic(provider, topic):
    pass

def act_upgrade_hp(self, theset):
    """unavailable in Models!:
    
    upgrade the hp by input a int """
    self.hp = theset
    self.save()
    return self.hp

def act_showindividual(id, c):
    '''
    this act is used for show lots of models
    such as Buyer Provider Order and User ETC.
    '''
    if c == 'buyer':
        r = act_showbuyer(id)
    elif c == 'provider':
        r = act_showprovider(id)
    elif c == 'order':
        r = act_showorder(id)
    elif c == 'user':
        r = act_showuser(id)
    # elif c == 'topic':
    #     r = ds_showtopic(id, bywhat)
    return r

def act_htmllogin(user):
    user = User.objects.get(id=user)
    log = ds_addlog(source=0, type=0, user=user, character=0)
    log.save()
    return "OK!" + "from " + "html " + log.user + " logged in"

def act_addlog(source, type, user, character):
    user = User.objects.get(id=user)
    log = Log(source=source,
        type=type,
        user=user,
        character=character)
    log.save()
    return "OK!" + "from " + log.source + log.user + " logged in"

def act_showsku(id):
    sku = Sku.objects.get(id=id)
    return sku

def act_getinfo(request):
    if request.user.is_authenticated():
        info = {
        'is_login': True,
        'current_user': request.user
        }
        timezone.activate(pytz.timezone("Asia/Shanghai"))
        info['now_tz'] = timezone.now()
        info['anotis'] =        act_getanotis(Notification.objects.filter(user=request.user, open_time__lte=timezone.now(), close_time__gte=timezone.now()).order_by('-open_time'))
        info['unread_anotis'] = act_getanotis(Notification.objects.filter(user=request.user, open_time__lte=timezone.now(), close_time__gte=timezone.now(), read=0).order_by('-open_time'))
        if request.user.provider.status == 0:
            info['is_provider'] = False
        else:
            info['is_provider'] = True
    else:
        info = {
        'is_login': False,
        }
    return info

def act_getanotis(notis):
    anotis = []
    for noti in notis:
        anoti = ds_getanoti(noti)
        anotis.append(anoti)
    return anotis

def act_addorder(skus, buyer):
    '''it will add a Order'''
    cny_price = ds_get_order_cny_price(skus)
    order = Order(cny_price=cny_price, buyer=buyer, type=OrderType.objects.get(id=1))
    order.save()
    order.skus = skus
    result = "Order added, need to pay: CNY¥"+ str(cny_price) +", this order includes: "+str(skus)
    return result

def act_booksku(sku_id, topic, buyer):
    sku = Sku.objects.get(id=sku_id)
    sku.topic = topic
    sku.status = '1'
    sku.save()
    sku.buyer.add(buyer)
    ds_noti_toprovider_skubooked(sku)
    result = "OK," + str(sku.topic) +" booked"

    return result

def act_generate_skus(provider, schedule):
    '''生成sku，schedule 是一个list，其中每一个item都是dict，包含 topic, start_time, end_time'''
    result=[]
    for item in schedule:
        result_item=''
        if item.get('topic') and item['start_time'] and item['end_time']:
            result_item=act_addsku(
                provider=provider,
                start_time=item['start_time'],
                end_time=item['end_time'],
                topic=item.get('topic'))
            result.append(result_item)
        elif item['start_time'] and item['end_time']:
            result_item=act_addsku(
                provider=provider,
                start_time=item['start_time'],
                end_time=item['end_time'])
            result.append(result_item)
    return result

# def act_cancelsku(sku_id, user):
#     sku = Sku.objects.get(id=sku_id)
#     sku.status = '8'
#     sku.save()
#     result = "OK," + str(sku.topic) +" is canceled, quite easy!"
#     type = 1 if sku.provider.user == user else 0
#     ds_noti_newcancel(sku=sku, user=user, type=type) 
#     return result

def act_provider_cancel_sku(sku, user):
    if sku.time_to_start() <= MIN_CANCEL_TIME:
        msg = _(u"马上开始了如果真要取消的话你自己练习学生做好解释工作，再找管理员取消吧。")
    elif sku.time_to_start() > MIN_CANCEL_TIME and sku.time_to_start() <= OK_CANCEL_TIME:
        sku.status = 3
        sku.save()
        ds_noti_tobuyer_noprovider(sku)
        msg = _(u"你是取消成功了，但是学生没法上课了，下回别这样了")
    else:
        if sku.buyer.exists():
            sku.status = 2
            sku.save()
            msg = _(u"恭喜，取消真轻松。你的学生会进入挽救池")
        else:
            sku.topic = None
            sku.status = 0
            sku.save()
            msg = _(u"虽然没有学生，但是也取消了")
    return msg


def act_buyer_cancel_sku(sku, user):
    if sku.status != (1 or 4):
            msg = _(u"Sorry, class status forbit you to cancel")
    else:
        if sku.buyer.count() > 1:
            # '''不知道remove对不对啊，好像是删掉这个buyer本身的意思'''
            sku.buyer.remove(user.buyer)
            msg = _(u"好了，这节课只有你不用来了，钱以后会打给你")
        elif sku.buyer.count() == 1:
            # 改成保留这个sku，保留证据！
            sku.status = 10
            sku.save()
            msg = _(u"好了，这节课没人会来了，钱以后会打给你")
            # 下面给这个老师再创建一个新的可约sku
            msg = msg + act_addsku(
                provider=sku.provider,
                start_time=sku.start_time,
                end_time=sku.end_time)
        ds_noti_toprovider_lostbuyer(sku=sku)
    return msg

def act_provider_repick(sku, new_provider):
    if sku.status == 2:
        msg=ds_change_provider(sku, new_provider)
        if sku.has_plan():
            sku.status = 5
        else:
            sku.status = 4
        sku.save()
    else:
        msg=_(u'这不是一节待抢课程。')
    return msg
def act_is_course_ready(sku):
     return True if sku.time_to_start() < BEFORE_COURSE_TIME else False