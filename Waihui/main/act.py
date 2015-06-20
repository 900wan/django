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

    result="OK!" + str(username) + "." + str(nickname) + "has added"
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

def act_addtopiccategory(name, url):
    topiccategory = TopicCategory(
        name = name,
        url = url)
    topiccategory.save()
    result = "OK, Topic category:" + name + " added!"
    return result

def act_addtopic(name, category_id, status, user_id):
    topic = Topic(
        name = name,
        category = category_id,
        status = status,
        creator = user_id)
    topic.save()
    result = "OK, Topic:" + name + " added!"
    return result

def act_addsku(provider_id, status, start_time, end_time, topic_id,):
    sku = Sku(
        provider = provider_id,
        status = status,
        start_time = start_time,
        end_time = end_time,
        topic = topic_id)
    sku.save()
    provider = Provider.objects.get(id = provider_id)
    topic = Topic.objects.get(id = topic_id)
    result = "OK, Sku:" + provider.name +"'s "+ topic.name + str(start_time) + " added!"
    return result

def act_addplan(sku_id, topic_id, status, content,):
    plan = Plan.objects(
        sku = sku_id,
        topic = topic_id,
        status = status,
        content = content)
    plan.save()
    sku = Sku.objects.get(id = sku_id)
    topic = Topic.objects.get(id = topic_id)
    result = "OK, Plan: " + sku.provider + topic.name + " added!"
    return result

def function():
    pass

def act_updatewallet():
    pass

def act_showuser(id):
    user = User.objects.get(id = id),
    return user