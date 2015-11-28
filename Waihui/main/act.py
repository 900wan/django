# -*- coding: utf-8 -*-
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
from main.ds import ds_addlog
from django.utils.translation import ugettext as _

def act_getlanguage(request):
    language = request.LANGUAGE_CODE
    # language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    return language

def act_signup(email, password, nickname, http_language, gender=1, mother_tongue_id=1, time_zone=1):
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
        gender=gender,
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

def act_addsku(provider, start_time, end_time, topic, buyer, status=1):
    '''it will add a Sku'''
    # provider = Provider.objects.get(id=provider_id)
    # topic = Topic.objects.get(id=topic_id)
    sku = Sku(
        provider=provider,
        status=status,
        start_time=start_time,
        end_time=end_time,
        topic=topic,
        )
    sku.save()
    sku.buyer.add(buyer)
    result = "OK, Sku:" + provider.name +"'s "+ topic.name + str(start_time) + " added! Student:" + buyer.nickname
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
    result = "OK, " + user.username + " left a message of" + content
    return result

def act_addorder(buyer_id, provider_id, cny_price, cny_paid):
    '''it will add a Order'''
    buyer = Buyer.objects.get(id=buyer_id)
    provider = Provider.objects.get(id=provider_id)
    order = Order(
        buyer=buyer,
        provider=provider,
        cny_paid=cny_paid,
        cny_price=cny_price,
        )
    order.save()
    result = "OK, " + Buyer.name + "place a order for" + provider.name + "costs " + cny_price
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
    else:
        info = {
        'is_login': False,
        }
    return info
