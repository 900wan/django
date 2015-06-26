# -*- coding: utf-8 -*-
from main.models import User
from main.models import Buyer
from main.models import Provider
from main.models import Topic
from main.models import TopicCategory
from main.models import Sku
from main.models import Plan
from main.models import Wallet
from main.models import Language
from main.models import ReplyToSku
from main.models import ReviewToProvider
from main.models import ReviewToBuyer

def act_signup(email,password,nickname,gender,mother_tongue_id,time_zone):
    # try:
    user = User.objects.create_user(
        username = email,
        email = email,
        password = password)
    user.save()

    buyer = Buyer(
        user = user,
        nickname = nickname,
        gender = gender,
        mother_tongue = Language.objects.get(id = mother_tongue_id),
        time_zone = time_zone)
    buyer.save()

    provider = Provider(
        user = user,
        status = 0,
        name = nickname)
    provider.save()

    wallet = Wallet(
        user = user)
    wallet.save()

    result="OK!" + str(email) + "." + str(nickname) + "has added"
    # except:
    #     pass
    return result

def act_addlanguage(chinese_name, english_name, local_name):
    language = Language(
        chinese_name = chinese_name,
        english_name = english_name,
        local_name = local_name,)
    language.save()
    result = "OK, Language:" + local_name + " added!"
    return result

def act_addTC(name, url):
    topiccategory = TopicCategory(
        name = name,
        url = url)
    topiccategory.save()
    result = "OK, Topic category:" + name + " added!"
    return result

def act_addtopic(name, category_id, status, user_id):
    topic = Topic(
        name = name,
        category = Category.objects.get(id = category_id),
        status = status,
        creator = User.objects.get(id = user_id))
    topic.save()
    result = "OK, Topic:" + name + " added!"
    return result

def act_addsku(provider_id, status, start_time, end_time, topic_id,):
    provider = Provider.objects.get(id = provider_id)
    topic = Topic.objects.get(id = topic_id)
    sku = Sku(
        provider = provider,
        status = status,
        start_time = start_time,
        end_time = end_time,
        topic = topic)
    sku.save()
    result = "OK, Sku:" + provider.name +"'s "+ topic.name + str(start_time) + " added!"
    return result

def act_addplan(sku_id, topic_id, status, content,):
    sku = Sku.objects.get(id = sku_id)
    topic = Topic.objects.get(id = topic_id)
    plan = Plan(
        sku = sku,
        topic = topic,
        status = status,
        content = content)
    plan.save()
    result = "OK, Plan: " + sku.provider + topic.name + " added!"
    return result

def act_addRTP(provider_id, buyer_id, sku_id, questionnaire, score):
    provider = Provider.objects.get(id = provider_id)
    buyer = Buy.objects.get(id = buyer_id)
    sku = Sku.objects.get(id = sku_id)
    RTP = ReviewToProvider(
        provider = provider,
        buyer = buyer,
        sku = sku,
        questionnaire = questionnaire,
        score = score)
    RTP.save()
    result = "OK, " + provider.name + "has leave a review on " + sku + "to " + buyer.name
    return result

def act_addRTB(provider_id, buyer_id, sku_id):
    provider = Provider.objects.get(id = provider_id)
    buyer = Buy.objects.get(id = buyer_id)
    sku = Sku.objects.get(id = sku_id)
    RTB = ReviewToBuyer(
        provider = provider,
        buyer = buyer,
        sku = sku,
        )
    RTB.save()
    result = "OK, " + provider.name + "has leave a review to " + buyer.name
    return result

def act_addRTS(user_id, type, content):
    user = User.objects.get(id = user_id)
    RTS = ReplytoSku(
        user = user,
        type = type,
        content = content,
        )
    RTS.save()
    result = "OK, " + user.name + " left a message of" + content
    return result

def act_addOrder(buyer_id, provider_id, cny_price, cny_paid):
    buyer = Buyer.objects.get(id = buyer_id)
    provider = Provider.objects.get(id = provider_id)
    order = Order(
        buyer = buyer,
        provider = provider,
        cny_paid = cny_paid,
        cny_price = cny_price,
        )
    RTS.save()
    result = "OK, " + buyer.name + "place a order for" + provider.name + "costs " + cny_price
    return result

def act_updatewallet():
    pass

def act_showuser(id):
    user = User.objects.get(id=id),
    return user

def act_showprovider(id):
    provider = Provider.objects.get(id=id)
    return provider

def act_showbuyer(id):
    buyer = Buyer.objects.get(id=id)
    return buyer

def act_showorder(id):
    order = Sku.objects.get(id=id)
    return order

def act_showindividual(id, c):
    if c == 'buyer':
        r = act_showbuyer(id)
    elif c == 'provider':
        r = act_showprovider(id)
    elif c == 'order':
        r = act_showorder(id)
    elif c == 'user':
        r = act_showuser(id)
    return r