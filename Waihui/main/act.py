# -*- coding: utf-8 -*-
from main.models import User
from main.models import Buyer
from main.models import Provider
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

    result="OK!" + str(user.username) + "." + str(buyer.nickname) + "has added"
    # except:
    #     pass
    return result

def act_addlanguage(chinese_name, english_name, local_name):
    language = Language(
        chinese_name = chinese_name,
        english_name = english_name,
        local_name = local_name,)
    language.save()
    result = "OK, " + local_name + " added!"
    return result

def act_showuser(id):
    user = User.objects.get(id = id),
    return user