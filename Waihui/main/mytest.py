# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.http import HttpResponse
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

def Test_skufunction(request):
    i = Sku.objects.get()
    return i