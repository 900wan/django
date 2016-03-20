 # -*- coding: utf-8 -*-
import pytz, json, datetime
from django.shortcuts import get_object_or_404, render
from django.utils import translation, timezone
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django import forms
# from login.models import User
from main.act import act_signup
# from main.act import act_jisuan
from main.act import act_addlanguage
from main.act import act_showuser
from main.act import act_showindividual
from main.act import act_addtopic
from main.act import act_htmllogin
from main.act import act_getlanguage
from main.act import act_addsku
from main.act import act_addrts
from main.act import act_addplan
from main.act import act_showsku
from main.act import act_getinfo
from main.act import act_getanotis
from main.act import act_addorder
from main.act import act_booksku
from main.act import act_generate_skus
from main.act import act_cancelsku
from main.act import act_provider_cancel_sku

from main.ds import  ds_getanoti

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

from main.mytest import Test_skufunction

def url_homepage(request):
    language = act_getlanguage(request)
    # user_language = language
    # translation.activate(user_language) 系统已经可以自动判断，这个激活暂时不需要
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    now_tz = timezone.now()
    info = act_getinfo(request)
    heading = _(u'Our hompage heading')
    return render(request, "main/home.html", locals())

def url_signup(request):
    '''用户通过浏览器将表单内容post到/signup/post后来到这里'''
    uf = SignupForm()
    language = act_getlanguage(request)
    msg = request.method + language
    if request.method == 'POST':
        uf = SignupForm(request.POST)
        if uf.is_valid():
            nickname = uf.cleaned_data['nickname']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            result = act_signup(password=password, nickname=nickname, email=email,
                http_language=language)
            msg = result + language
    info = act_getinfo(request)
    return render(request, "main/signup.html", {'info':info, 'form':uf, 'msg':msg})
    # act_signup()

def url_login(request):
    uf = LoginForm(request.POST)
    msg = ''
    next = ''
    info = act_getinfo(request)
    if request.GET:  
       next = request.GET['next']
    if request.method == 'POST':
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    info = act_getinfo(request)
                    if next == '':
                        return render(request, "main/right.html", {'info':info, 'username':username})
                    else:
                        return HttpResponseRedirect(next)
                else:
                    msg = _(u'Login failed, user is not active.')
                    return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})
            else:
                msg = _(u'Guess what? Login failed.')
                return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})
        else:
            msg = _(u'form not valid')
            return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg})
        # elif uf.is_valid():
        #     name=uf.cleaned_data['name']
        #     return render(request, 'main.test_result.html',{'uf':uf})
    else:
        return render(request, "main/login.html", {'info':info, 'uf':uf, 'msg':msg, 'next':next})

# @login_required
def url_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:home'))

def url_tc(request, offset_id):
    return HttpResponse(offset_id)

def url_tutor(request, offset_id):
    '''For show tutor home page'''
    id = int(offset_id)
    act = act_showindividual(id, 'provider')
    return HttpResponse(act.status)

@login_required
def url_holdsku(request):
    '''make a sku for order, One order can have many skus'''
    info = act_getinfo(request)
    current_user = info['current_user'] 
    skus = Sku.objects.all()
    msg = request.method+", user: ["+str(current_user.username)+"], user's buyer: ["+str(current_user.buyer)+"]"
    if request.method == 'POST':
        uf = HoldSkuForm(request.POST)
        if uf.is_valid():
            provider = uf.cleaned_data['provider']
            topic = uf.cleaned_data['topic']
            start_time = uf.cleaned_data['start_time']
            end_time = uf.cleaned_data['end_time']
            result = act_addsku(provider=provider, topic=topic, start_time=start_time, end_time=end_time, buyer=current_user.buyer)
            msg = result
    else:
        uf = HoldSkuForm()    
    return render(request, "main/addsku.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"add sku", 'skus':skus})
    # teachers = Provider.objects.all()
    # topics = Topic.objects.all()
    # 
    # return render(request, "main/addsku.html", {'teacher_list':teachers, 'topic_list':topics,})

def url_order(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'order')
    return HttpResponse(act)

def url_lesson_prepare(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_summarize(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_lesson_rate(request, offset_id):
    id = int(offset_id)
    act = act_showindividual(id, 'sku')
    return HttpResponse(act)

def url_classroom(request):
    pass

def url_user(request,offset_id):
    id = int(offset_id)
    user = act_showindividual(id, 'user')
    usern = user.username
    email = user.email 
    password = user.password
    result = usern + email + password
    return HttpResponse(result)

@login_required
def url_replytosku(request, sku_id):
    '''handling the replys to sku,'''
    info = act_getinfo(request)
    current_user = info['current_user']
    sku = Sku.objects.get(id=sku_id)
    uf = AddRTSForm(request.POST)
    uf.fields['reply_to'].queryset = ReplyToSku.objects.filter(sku=sku)
    is_involved = (current_user.provider == sku.provider) or (sku.buyer.filter(id=current_user.buyer.id).exists())
    if is_involved:
        msg = request.method
        if request.method == 'POST':
            if uf.is_valid():
                content = uf.cleaned_data['content']
                replyto = uf.cleaned_data['reply_to']
                if current_user.provider == sku.provider:
                    type = 1    
                else:
                    type = 0
                result = act_addrts(user=current_user, type=type, content=content, reply_to=replyto, sku=sku)
                msg = result
            else:
                msg = "validation failed"
        else:
            pass
    else:
        msg = 'you are not involved in this class'
    return render(request, "main/addrts.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"Reply to Sku", 'sku_id':sku.id, 'is_involved':is_involved})

@login_required
def url_addplan(request, sku_id):
    info = act_getinfo(request)
    current_user = request.user
    uf = AddPlanForm(request.POST)
    sku = Sku.objects.get(id=sku_id)
    if current_user != sku.provider.user:
        msg = "no"
    else:
        msg = request.method
        topic = sku.topic
        sku.status = 4
        sku.save()
        if request.method == 'POST':
            if uf.is_valid():
                status = uf.cleaned_data['status']
                content = uf.cleaned_data['content']
                assignment = uf.cleaned_data['assignment']
                slides = uf.cleaned_data['slides']
                roomlink = uf.cleaned_data['roomlink']
                materiallinks = uf.cleaned_data['materiallinks']
                materialhtml = uf.cleaned_data['materialhtml']
                voc = uf.cleaned_data['voc']
                copy_from = uf.cleaned_data['copy_from']
                sumy = uf.cleaned_data['sumy']
                result = act_addplan(sku=sku, topic=topic, status=status, content=content, 
                    assignment=assignment, slides=slides, roomlink = roomlink, materialhtml=materialhtml, materiallinks=materiallinks, voc=voc,
                    copy_from=copy_from, sumy=sumy)
                msg = result
    return render(request, "main/addplan.html", {'info':info, 'uf':uf, 'msg':msg, 'heading':"Add a plan on SKU", 'sku':sku})

@login_required
def url_showsku(request, sku_id): 
    info = act_getinfo(request)    
    current_user = info['current_user']
    sku = act_showsku(int(sku_id))
    is_involved = (current_user.provider == sku.provider) or (sku.buyer.filter(id=current_user.buyer.id).exists())
    try:
        plan = sku.plan
        has_plan = True
    except Plan.DoesNotExist:
        plan = ""
        has_plan = False
    rtss = ReplyToSku.objects.filter(sku=sku)
    is_provider = True if current_user == sku.provider.user else False
    msg = str(request)
    return render(request, "main/showsku.html", {'info':info, 'heading':"SKU #"+str(sku.id), 'msg':msg, 'is_provider':is_provider, 'is_involved':is_involved, 'sku':sku, 'has_plan':has_plan,'plan':plan, 'rtss':rtss})

def url_skulist(request):
    # timezone.activate(pytz.timezone("Asia/Shanghai"))
    info = act_getinfo(request)
    skus = Sku.objects.all()
    msg = str(request)
    return render(request, "main/skulist.html", {'info':info, 'heading':"There is a Sku list", 'msg':msg, 'skus':skus})

def url_order_add(request, skus):
    info = act_getinfo(request)
    current_user = info['current_user']
    for i in skus:
        thesku = Sku.objects.filter(id=i)
        thesku.status = 2


def url_test(request):
    i = Sku.objects.get(id=7)
    a = i.duration()
    b = a['seconds']
    return render(request, "main/mytest.html", {'i':i, 'a':a, 'b':b})

def url_idtest(request, set_id):
    result = Test_skufunction(set_id)
    return render(request, "main/mytest", {'result':result})

@login_required
def url_dashboard(request):
    info = act_getinfo(request)
    return render(request, "main/dashboard.html",locals())

@login_required
def url_office(request):
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    info = act_getinfo(request)
    return render(request, "main/office.html",locals())

@login_required
def url_notifications(request):
    info = act_getinfo(request)
    upcomming_anotis = act_getanotis(Notification.objects.filter(user=info['current_user'],open_time__gt=timezone.now()).order_by('-open_time'))
    past_anotis = act_getanotis(Notification.objects.filter(user=info['current_user'],close_time__lt=timezone.now()).order_by('-open_time'))
    return render(request, "main/notifications.html",locals())

@login_required
def url_notification_go(request, noti_id):
    info = act_getinfo(request)
    noti = get_object_or_404(Notification ,id=noti_id)
    if noti.user == info['current_user']:
        if noti.read == 0:
            noti.read = 1
            noti.save()
        return HttpResponseRedirect(ds_getanoti(noti)['link'])
    else:
    # 这说明这条noti不属于当前用户，无权查看的
        return HttpResponse('这条消息不属于当前用户，无权查看。')

@login_required
def url_addorder(request):
    '''add a order '''
    info = act_getinfo(request)
    buyer = info['current_user'].buyer
    uf = OrderForm(request.POST)
    uf.fields['skus'].queryset = Sku.objects.filter(buyer=buyer)
    if request.method == 'POST':
        if uf.is_valid():
            skus = uf.cleaned_data['skus']
            # msg=skus
            msg = act_addorder(skus,buyer)
    # result = act_addorder(skus, buyer)
    # uf = OrderForm(request.POST)
    # uf.fields['skus'].queryset = Sku.objects.filter(buyer=info['current_user'].buyer)
    
    return render(request, "main/addorder.html", locals())

@login_required
def url_addsku(request):
    info = act_getinfo(request)
    current_user = info['current_user']
    skus = Sku.objects.all()
    if current_user.provider.status == 0:
        msg = "You have no rights to add class, Please be a teacher first."
    else:
        msg = request.method+", Provider: ["+str(current_user.username)+"]"
        if request.method == 'POST':
            uf = AddSkuForm(request.POST)
            if uf.is_valid():
                start_time = uf.cleaned_data['start_time']
                end_time = uf.cleaned_data['end_time']
                topic = uf.cleaned_data['topic']
                result = act_addsku(provider=current_user.provider, start_time=start_time, end_time=end_time, topic=topic)
                msg = result
        else:
            uf = AddSkuForm()
    return render(request, "main/addsku.html", locals())

def url_picktopic(request):
    info = act_getinfo(request)
    topics = Topic.objects.all()
    skus = Sku.objects.all()
    no_topics = Sku.objects.filter(topic=None)
    return render(request, 'main/picktopic.html', locals())

def url_skuintopic(request, topic_id):
    info = act_getinfo(request)
    skus_with_topics = Sku.objects.filter(topic_id=topic_id, buyer=None)
    skus_without_topics = Sku.objects.filter(topic=None, buyer=None)
    skus = skus_with_topics|skus_without_topics
    topic = Topic.objects.get(id=topic_id)
    return render(request, 'main/skuintopic.html', locals())

@login_required
def url_booksku(request, sku_id, topic_id):
    info = act_getinfo(request)
    uf = BookSkuForm(request.POST)
    if request.method == 'POST':
        if uf.is_valid():
            topic = Topic.objects.get(id=topic_id)
            buyer = info['current_user'].buyer
            result = act_booksku(sku_id=sku_id, topic=topic, buyer=buyer)
            msg = result
            return render(request, 'main/result.html', locals())   
    msg = str(request.POST) 
    return render(request, 'main/booksku.html', locals())

@login_required
def url_bookresult(request):
    info = act_getinfo(request)
    msg = request.POST
    return render(request, 'main/bookresult.html', locals())

@login_required
def url_schedule(request):
    info = act_getinfo(request)
    timezone.activate(pytz.timezone("Asia/Shanghai"))
    tz = timezone.get_current_timezone()
    now_tz = timezone.now()
    info = act_getinfo(request)    
    current_user = info['current_user']
    provider = current_user.provider
    msg=''
    if info['is_provider']:
        if request.method == 'POST':
            uf = ScheduleForm(request.POST)
            if uf.is_valid():
                raw_schedule_json = uf.cleaned_data['schedule']
                set_provider = uf.cleaned_data['provider']
                raw_schedule=json.loads(raw_schedule_json)
                schedule=[]
                for raw_item in raw_schedule:
                    item={}
                    try:
                        if raw_item.get('topic_id'):
                            item['topic']=Topic.objects.get(id=int(raw_item.get('topic_id')))
                        item['start_time']=tz.localize(datetime.datetime.strptime(raw_item['start_time'],"%Y-%m-%d %H:%M:%S"))
                        if raw_item.get('end_time'):
                            item['end_time']=tz.localize(datetime.datetime.strptime(raw_item['end_time'],"%Y-%m-%d %H:%M:%S"))
                        else:
                            item['end_time']=tz.localize(datetime.datetime.strptime(raw_item['start_time'],"%Y-%m-%d %H:%M:%S")+datetime.timedelta(minutes=30))
                        if item['start_time'] and (item['start_time']>now_tz):
                            schedule.append(item)
                    except Exception, e:
                        raise e
                # msg=schedule
                msg=act_generate_skus(provider, schedule)
        else:
            uf = ScheduleForm(initial = {'provider': provider })
        return render(request,"main/schedule.html", locals())
    else:
    # 这说明这个人不是老师
        return HttpResponse('You are not an authenticated tutor. 你不是教师，无权访问此页')

@login_required
def url_bcancelsku(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if sku.buyer.filter(id=info['current_user'].buyer.id).exists():
        uf = CancelSkuForm(request.POST)
        uf.fields['sku'].queryset = Sku.objects.get(id=sku_id)
        if request.method == 'POST':
            if uf.is_valid():
                result = act_cancelsku(sku_id=sku_id, user=info['current_user'])
                msg = result
                return render(request, 'main/result.html', locals())
    msg = str(request.POST)
    return render(request, "main/buyer_cancelsku.html", locals())

@login_required
def url_provider_cancel_sku(request, sku_id):
    info = act_getinfo(request)
    sku = Sku.objects.get(id=sku_id)
    if sku.provider.user == info['current_user']:
        if sku.status == 1:
            # 视作无伤害取消
            msg = act_provider_cancel_sku(sku, info['current_user'])
        elif sku.status == 4:
            # 视作有伤害取消
            msg = act_provider_cancel_sku(sku, info['current_user'])
        else:
            msg = _("这个课程的状态不适合取消")
    else:
        msg = _("对不起，不是老师不能取消")
    return render(request, "main/result.html", locals())
