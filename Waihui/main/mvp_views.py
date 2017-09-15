 # -*- coding: utf-8 -*-
import pytz, json, datetime
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from main.act import act_signup
from main.act import act_userlogin
from main.act import act_addlanguage
from main.act import act_showuser
from main.act import act_showindividual
from main.act import act_addtopic
from main.act import act_htmllogin
from main.act import act_getlanguage
from main.act import act_addsku
from main.act import act_addrts
from main.act import act_addplan
from main.act import act_getinfo
from main.act import act_getanotis
from main.act import act_addorder
from main.act import act_booksku
from main.act import act_assignid_sku_topic
from main.act import act_generate_skus
from main.act import act_provider_cancel_sku
from main.act import act_buyer_cancel_sku
from main.act import act_provider_repick
from main.act import act_provider_ready_sku
from main.act import act_buyer_ready_sku
from main.act import act_expand_skus
from main.act import act_expand_orders
from main.act import act_edit_provider_profile
from main.act import act_upload_provider_avatar
from main.act import act_buyer_feedback_sku
from main.act import act_provider_feedback_sku
from main.act import act_buyer_cancel_order
from main.act import act_htmllogout
from main.act import act_orderpaid

from main.ds import  ds_getanoti

from main.models import User
from main.models import Language
from main.models import Provider
from main.models import Buyer
from main.models import Topic
from main.models import Sku
from main.models import ReplyToSku
from main.models import Plan
from main.models import Notification
from main.models import Order

from main.forms import LoginForm
from main.forms import SignupForm
from main.forms import AddSkuForm
from main.forms import AddRTSForm
from main.forms import AddPlanForm
from main.forms import OrderForm
from main.forms import HoldSkuForm
from main.forms import BookSkuForm
from main.forms import ScheduleForm
from main.forms import CancelSkuForm
from main.forms import RoomlinkForm
from main.forms import ProviderProfileForm
from main.forms import ProviderAvatarForm
from main.forms import ProviderFeedbackSkuForm
from main.forms import BuyerFeedbackSkuForm
from main.forms import PlaceSkuForm

def home(request):
    language = act_getlanguage(request)
    info = act_getinfo(request)
    return render(request, "mvp/home.html", locals())


def dashboard(request):
    language = act_getlanguage(request)
    info = act_getinfo(request)
    return render(request, "mvp/dashboard.html", locals())