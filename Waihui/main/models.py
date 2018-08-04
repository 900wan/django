# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# from main.act import act_upgrade_hp
# 无法导入acts
BEFORE_COURSE_TIME = datetime.timedelta(minutes=15)

def upgrade_hp(self,theset):
    """upgrade the hp by input a int """
    self.hp = theset
    self.save()
    return self.hp

def upgrade_status(self,theset):
    """upgrade the hp by input a int """
    self.status = theset
    self.save()
    return self.status

# Create your models here.
# index 1
class Language(models.Model):

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __unicode__(self):
        return u'%s' % self.english_name
    chinese_name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    # 需要修改english_name为系统可识别
    local_name = models.CharField(max_length=50)
    def autoaddlanguage(self, language_name):
        self.english_name = get_language()
        self.save()
        return self.english_name




# index 2
class Provider(models.Model):
    """
    There are user(o2o), status(mc), name(mc), weekday_pattern(mcoseint), fee_rate(mfloat), hp(mfloat),hp(mfloat)
    and get_fee_rate(), upgrade_status(int), upgrade_hp(int), set_weekday_pattern()
    in Provider model
    """
    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        db_tablespace = "ImageStore"

    def __unicode__(self):
        return u'%s' % self.name
    user = models.OneToOneField(User)

    LEVELS_OF_TEACHER_CHOICES = (
        (0, '非教师'),
        (1, '已申请'),
        (2, '实习'),
        (3, '正式'),
        )
    status = models.IntegerField(
        choices=LEVELS_OF_TEACHER_CHOICES,
        default=0,
        )
    name = models.CharField(max_length=50, )
    weekday_pattern = models.CharField(max_length=200, blank=True, null=True, validators=[validate_comma_separated_integer_list])
    fee_rate = models.FloatField(default=1)
    hp = models.FloatField(default=100) #教师活跃度
    teaching_language = models.ManyToManyField(Language, blank=True)
    bio = models.TextField(blank=True)
    video = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="provider_avatars/%Y/%m/%d/", default='/media/none/a.png', blank=True, null=True)
    assigned_location = models.TextField(blank=True, null=True)
    assigned_nationality = models.TextField(blank=True, null=True)
    active_daily = models.IntegerField(default=10, blank=True, null=True)
    active_course = models.IntegerField(default=60, blank=True, null=True)
    active_community = models.IntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def clean(self, *args, **kwargs):
        '''setting the limitation of 
        provider active series value
        '''
        # add custom validation here
        if self.active_daily > 10:
            self.active_daily = 10
        elif self.active_daily <0:
            self.active_daily = 0

        elif self.active_course > 90:
            self.active_course =90
        elif self.active_course < 0:
            self.active_course = 0

        elif self.active_community > 5:
            self.active_community =5
        elif self.active_community < 0:
            self.active_community = 0

        super(Provider, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Provider, self).save(*args, **kwargs)

    def get_fee_rate(self):
        """对该老师的fee_rate进行更新（在需要时）"""
        if self.fee_rate == '':
            return "empty value"
        else:
            return '%s' %(self.fee_rate)
        self.save()
        return self.fee_rate
    def upgrade_status(self, theset):
        """对教师状态进行升级"""
        # if form is OK
        return upgrade_status(self, theset)
    def upgrade_hp(self, theset):
        '''upgrade hp of teacher'''
        # user.last_login
        d1 = datetime.datetime.now()
        d2 = self.modified
        if (d1-d2).days >= 1:
            return "in if"
        return upgrade_hp(self, theset)

    def set_weekday_pattern(self, theset):
        pass

    # @receiver(post_save, sender=Log)
    # def log_save(sender, instance, created, **kwargs):
    #     if created:
    #         log = instance
    #         log.activity_change
    #         actlog = ActLog(
    #             log=instance,
    #             buyer_hp=instance.user.buyer.hp,
    #             provider_active_daily=instance.user.provider.active_daily,
    #             provider_active_course=instance.user.provider.active_course,
    #             provider_active_community=instance.user.provider.
    #             active_community)
    #         actlog.save()

# index 3
class Buyer(models.Model):

    class Meta:
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"

    def __unicode__(self):
        return u'%s' % self.nickname
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50)
    MALE = 0
    FEMALE = 1
    CHOICES_OF_GENDER = (
        (MALE, '男'),
        (FEMALE, '女'),
        )
    gender = models.IntegerField(
        choices=CHOICES_OF_GENDER,
        blank=True, null=True,
        )
    brithday = models.DateField(blank=True, null=True)
    mother_tongue = models.ForeignKey(Language, blank=True, null=True)
    time_zone = models.CharField(max_length=50)
    hp = models.IntegerField(default=100)
    provider = models.ForeignKey(Provider, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    nationality = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    # last_activity.editable = True
    def set_provider(self, provider):
        new_provider = provider
        self.provider = new_provider
        return u'%s' %self.provider

# index 4
class TopicCategory(models.Model):

    class Meta:
        verbose_name = "TopicCategory"
        verbose_name_plural = "TopicCategorys"

    def __unicode__(self):
        return u'%s' % self.name
    name = models.CharField(max_length=50, blank=True, null=True)
    background_image = models.URLField()

# index 5
class Topic(models.Model):

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __unicode__(self):
        return u'%s' % self.name
    name = models.CharField(max_length=50)
    desc = models.TextField()
    category = models.ForeignKey(TopicCategory)
    # default_plan = models.ForeignKey(Plan,blank=True,null=True)
    status = models.IntegerField()
    creator = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 6
class Sku(models.Model):

    class Meta:
        verbose_name = "Sku"
        verbose_name_plural = "Skus"
        # ordering = ['-start_time']

    def __unicode__(self):
        if self.topic is None:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+"no topic")
        else:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+str(self.topic))
    provider = models.ForeignKey(Provider, )
    buyer = models.ManyToManyField(Buyer, blank=True)

    STATUS_OF_SKU_CHOICES = (
        (0, _(u'可约')), #定教师没学生,教师生成sku，等待学生预约
        (1, '已约'), #学生完成付费预约，等待教师确认
        (2, '待抢'), #教师取消，等待新教师接单
        (3, '没有教师了'), #来不及换老师了。。。
        (4, '已定'), #教师确认学生的预约
        (5, '已备课'),
        (6, '老师ready'),
        (7, '学生进了教室'),
        (8, '待评价'), #学生评价老师
        (9, '已结束 '),
        (10, '学生取消'),
        # (11, '教师完成课后作业') #接下来学生评价老师，接8
    )

    status = models.IntegerField(
        choices=STATUS_OF_SKU_CHOICES,
        default=0,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    topic = models.ForeignKey(Topic, verbose_name=_(u'话题'), blank=True, null=True)
    # payoff = models.ForeignKey(ProviderPayoff, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def duration(self):
        duration = (self.end_time - self.start_time)
        duration = {
        'Total':duration,
        'hours':duration.seconds//3600,
        'minuets':(duration.seconds % 3600) // 60,
        'seconds':duration.seconds % 60,
        }
        return duration
    def has_plan(self):
        try:
            plan = self.plan
            has_plan = True
        except Plan.DoesNotExist:
            has_plan = False
        return has_plan
    def time_to_start(self):
        return self.start_time - timezone.now()
    def further(self):
        if self.start_time > timezone.now():
            return self

# index 7
class Plan(models.Model):
    '''
    
    '''
    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __unicode__(self):
        return u'Plan of %s' % self.sku
    sku = models.OneToOneField(Sku, blank=True, null=True)
    topic = models.ForeignKey(Topic)
    # 给sku：
    # 已备课；已上完；
    # 给topic：
    # 待审核；成功通过；失败待修改
    # 2018.3.6:提出修改建议，简化至4个状态，不做对于Topic的区分。
    CHOICES_OF_STATUS = (
        (0, _(u'未备课')),
        (1, _(u'待审核')),
        (2, _(u'未通过')),
        (3, _(u'已备课')),
        )
    status = models.IntegerField(_(u'教案状态'), choices=CHOICES_OF_STATUS)
    content = models.TextField(_(u'课程大纲'))
    assignment = models.TextField(_(u'课后作业'), blank=True, null=True)
    slides = models.TextField(_(u'课件'), blank=True, null=True)
    materiallinks = models.TextField(_(u'课件链接'), blank=True, null=True)
    materialhtml = models.TextField(_(u'课件网页'), blank=True, null=True)
    voc = models.TextField(_(u'生词'), blank=True, null=True)
    copy_from = models.ForeignKey('self', verbose_name=_(u'源自'), blank=True, null=True)
    # summary 写sum我怕出问题
    sumy = models.TextField(_(u'总结'), blank=True, null=True)
    roomlink = models.URLField(_(u'上课链接'), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 8
class Wallet(models.Model):

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __unicode__(self):
        return u'%s' % self.cny_balance
    user = models.OneToOneField(User)
    cny_balance = models.FloatField(default=0)
    display_currency = models.CharField(default="CNY", max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def upgragde_balance(self, theset, order):
        if order == 0:
            self.cny_balance = theset
        elif order.status == 1:
            amount = order.cny_price
            self.cny_balance -= amount
        self.save()
        return self.cny_balance

# index 9
class ReviewToProvider(models.Model):
    '''用于学生评价教师。同时，存在多个学生评价同一个课程的情况'''
    class Meta:
        verbose_name = "ReviewToProvider"
        verbose_name_plural = "ReviewToProviders"

    def __unicode__(self):
        return u'%s' % 'ReviewToProvider SkuID:[' + str(self.sku.id) + ']' + ' Score:[' + str(self.score) + '] ' +str(self.buyer.nickname) + ' reviews to ' + str(self.provider.name) + ' on SkuID:[' + str(self.sku.id) + ']'
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.ForeignKey(Sku)
    questionnaire = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=250, blank=True, null=True) #此处倾向于记录后台对教师的评语
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 10
class ReviewToBuyer(models.Model):

    class Meta:
        verbose_name = "ReviewToBuyer"
        verbose_name_plural = "ReviewToBuyers"

    def __unicode__(self):
        return u'%s' % 'SkuID:[' + str(self.sku.id) + ']' + str(self.provider.name) + ' reviews to ' + str(self.buyer.nickname)
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.ForeignKey(Sku)
    questionnaire = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class FeedbackQuestionnaireB2P(models.Model):

    class Meta:
        verbose_name = "Questionnaire of Feedback from Buyer to Provider"
        verbose_name_plural = "Questionnaires of Feedback from Buyer to Provider"

    def __str__(self):
        return str(self.rtp)

    CHOICES_OF_SATISFACTION = (
        # (0, _(u'已失效')),
        (1, _(u'0星')),
        (2, _(u'1星')),
        (3, _(u'2星')),
        (4, _(u'3星')),
        (5, _(u'4星')),
        (6, _(u'5星')),
        )
    CHOICES_OF_PLAN = (
        # (0, _(u'已失效')),
        (1, _(u'条理清楚')),
        (2, _(u'只是还可以')),
        (3, _(u'完全看不懂他要讲什么')),
        )
    CHOICES_OF_TEACHING = (
        # (0, _(u'已失效')),
        (1, _(u'非常清楚')),
        (2, _(u'一般，勉强听懂')),
        (3, _(u'不清楚')),
        )
    CHOICES_OF_CONTINUING = (
        # (0, _(u'已失效')),
        (1, _(u'十分愿意')),
        (2, _(u'值得考虑')),
        (3, _(u'不会了，再也不会了')),
        )
    satisfaction = models.IntegerField(_(u'本次课程你对老师是否满意'), choices=CHOICES_OF_SATISFACTION, null=True)
    plan = models.IntegerField(_(u'教案是否清楚明白'), choices=CHOICES_OF_PLAN, null=True)
    teaching = models.IntegerField(_(u'老师讲课是否清楚明白'), choices=CHOICES_OF_TEACHING, null=True)
    continuing = models.IntegerField(_(u'你还会选这个老师的课程吗'), choices=CHOICES_OF_CONTINUING, null=True)
    comment = models.TextField(_(u'用一句话评价一下这次的课程'))
    rtp = models.ForeignKey(ReviewToProvider)


# index 11
class ReplyToSku(models.Model):

    class Meta:
        verbose_name = "ReplyToSku"
        verbose_name_plural = "ReplyToSkus"

    TYPE_OF_CONTENT = (
        (0, _(u'闲聊')),
        (1, _(u'问题')),
    )


    def __unicode__(self):
        return u'%s' % self.content
    sku = models.ForeignKey(Sku)
    user = models.ForeignKey(User)
    type = models.IntegerField()
    content = models.TextField()
    content_type = models.IntegerField(choices=TYPE_OF_CONTENT)
    reply_to = models.ForeignKey('self', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 12
class OrderType(models.Model):

    class Meta:
        verbose_name = "OrderType"
        verbose_name_plural = "OrderTypes"

    def __unicode__(self):
        return u'%s' % self.type
    type = models.CharField( max_length=50)

# index 13
class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __unicode__(self):
        return _(u'[ %(id)s ] Order of %(buyer)s contains %(len)s skus, cost %(cny_price)s Yuan') % {'id':self.id, 'buyer':self.buyer, 'len':len(self.skus.all()), 'cny_price':self.cny_price}

    buyer = models.ForeignKey(Buyer)
    provider = models.ForeignKey(Provider, null=True)
    cny_price = models.FloatField()
    cny_paid = models.FloatField(default=0)
    pay_method = models.CharField(blank=True, null=True, max_length=50)
    skus = models.ManyToManyField(Sku, blank=True)
    skus_topic = models.CharField(blank=True, null=True, max_length=300)
    type = models.ForeignKey(OrderType)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paidtime = models.DateTimeField(null=True, blank=True) #付款日期
    paidbacktime = models.DateTimeField(null=True, blank=True) #退款日期
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    # 不可支付、未支付、已支付、已完成、申请退款、已退款……

    STATUS_OF_ORDER_TYPE = (
        (0, '不可支付'),
        (1, '未支付'),
        (2, '已支付'),
        (3, '已完成'),
        (4, '申请退款'),
        (5, '已退款'),
        (6, '已取消'),#页面显示为cancel
    )

    status = models.IntegerField(
        choices=STATUS_OF_ORDER_TYPE,
        default=1)

    def upgrade_status(self, theset):
        """对order状态进行升级"""
        self.status = theset
        self.save()

    def time_to_pay_24hours(self):
        '''剩余余款时间 时限设置为24小时'''
        return self.created - timezone.now() + datetime.timedelta(hours=24)

    def time_to_pay(self, timedelta):
        '''剩余余款时间 时限设置为24小时'''
        return self.created - timezone.now() + datetime.timedelta(timedelta)

class Log(models.Model):
    '''Model Log is for record of the journal of a User daily action.
    To record this info, you should insert log attribution in Front'''
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __unicode__(self):
        return u'%s' % '['+str(self.user.username)+'] '+ self.get_action_display() + ' on ' + self.get_client_display() + ' as ' + str(self.get_character_display()) + ' at ' + str(self.created)


    TYPE_OF_CLIENT = (
        (0, '网页端'),
        (1, '移动网页端'),
        (2, 'IOS客户端'),
        (3, '安卓客户端')
    )
    client = models.IntegerField(
        choices=TYPE_OF_CLIENT,
        default=0)

    TYPE_OF_ACTION = (
        (0, '登陆'),
        (1, '登出'),
        (2, '下单'),
        (3, '修改'),
        (4, '取消'),
        (5, '计算劳资'),
        (6, '提取工资'),
        (7, _(u'浏览')),
        (8, _(u'更新课表')),
        (9, _(u'学生订课')), #认为时完成订单支付以后
        (10, _(u'教师接单')),
    )
    action = models.IntegerField(choices=TYPE_OF_ACTION)

    TYPE_OF_ACTIVITY_ACTION = (
        (10, _(u"登陆(+1)")),
        (-10, _(u"超24h未登陆(-2)")),
        (20, _(u"星期五24点前更新下周课表(+1)")),
        (21, _(u"1h内确认接单（+1）")),
        (22, _(u"上完课（+1）")),
        (23, _(u"上完课15分钟内完成教师评价（+1）")),
        (24, _(u"结束课程后1h内更新病例（+1）")),
        (25, _(u"trial lesson后首次编写学生病例（+1）")),
        (26, _(u"抢单（+5）")),
        (-20, _(u"未及时更新课表（-5）")),
        (-21, _(u"5小时内未接单或取消订单（-15）")),
        (-22, _(u"放弃订单（-20）")),
        (-23, _(u"抢单除外没提前24小时备课（-10）")),
        (-24, _(u"没去上课（-30）")),
        (-25, _(u"迟到（-5）")),
        (30, _(u"30min内回答学生问题（+1）")),
        (-30, _(u"未回答学生问题（-2）")),

    )
    activity_action = models.IntegerField(choices=TYPE_OF_ACTIVITY_ACTION, null=True, blank=True)

    activity_change = models.IntegerField(null=True, blank=True)
    pre_value = models.IntegerField(null=True, blank=True)
    addtional_title = models.CharField(null=True, blank=True, max_length=50)
    addtional_value = models.CharField(null=True, blank=True, max_length=50)
    addtional_content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)
    order = models.ForeignKey(Order, null=True, blank=True)
    sku = models.ForeignKey(Sku, on_delete=models.CASCADE, null=True, blank=True)
    info_json = models.TextField(null=True, blank=True)
    TYPE_OF_CHARACTER = (
        (0, 'buyer'),
        (1, 'provider'))
    character = models.IntegerField(choices=TYPE_OF_CHARACTER, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_pre_act_log(self, activity_action=None, activity_change=None):
        '''return pre log under spec activity of this very user'''
        try:
            pre_log = self.get_previous_by_created(activity_action=activity_action, user=self.user,
                                                   activity_change=activity_change)
            # if pre_log.created.date() == timezone.now().date():
            #     pre_log = None
            #     assert False
        except:
            pre_log = None

        return pre_log

    def act_log_check(self):
        '''return activity action by checked the static'''
        activity_action = None
        istoday10 = None
        mistoday10 = None
        istoday = False
        prov_lc = self.user.buyer.last_activity
        interval_time = timezone.now() - prov_lc
        gth24 = interval_time > datetime.timedelta(hours=24)
        try:
            pre_10_log = self.get_pre_act_log(activity_action=10)
            pre_10_log = self.get_previous_by_created(activity_action=10, user=self.user)
            istoday10 = pre_10_log.created.date() == timezone.now().date()
        except:
            pre_10_log = None

        try:
            pre_m10_log = self.get_pre_act_log(activity_action=-10)
            pre_m10_log = self.get_previous_by_created(activity_action=-10, user=self.user)
            mistoday10 = pre_m10_log.created.date() == timezone.now().date()
        except:
            pre_m10_log = None
        if mistoday10 or istoday10:
            istoday = True
        if gth24:
            activity_action = -10
            i = interval_time.total_seconds() // (24*3600)
            j = interval_time.total_seconds() //3600
            k = j //24
            activity_change = -2*i
            if pre_m10_log is not None:
                if istoday:
                    activity_action = None
        else:
            if pre_10_log is not None:
                if not istoday:
                    activity_action = 10
                    activity_change = 1
                else:
                    activity_action = None
            if pre_m10_log is not None:
                if istoday:
                    activity_action = None
        if activity_action is None:
            return None

        self.activity_action = activity_action
        self.activity_change = activity_change
        log = self.save()
        # assert False
        return log

    def save(self, *args, **kwargs):
        if self.activity_action:
            provider = self.user.provider
            series_num = str(abs(self.activity_action))[0]
            # the series number(first charactor) of action is sorted
            if series_num == 1:
                provider.active_daily += self.activity_change
            elif series_num == 2:
                provider.active_course += self.activity_change
            elif series_num == 3:
                provider.active_community += self.activity_change
            provider.save()
        super(Log, self).save(*args, **kwargs)

    # def act_log_check(self):
    #     '''return activity action by checked the static'''
    #     try:
    #         pre_log = self.get_previous_by_created(user=self.user)
    #         interval_time = self.created - pre_log.created
    #     except:
    #         pre_log = None
    #     try:
    #         pre_m10_log = self.get_pre_act_log(activity_action=-10)
    #         pre_m10_log = self.get_previous_by_created(activity_action=-10, user=self.user)
    #     except:
    #         pre_m10_log = None
    #     activity_action = None
    #     pre_10_log = self.get_pre_act_log(
    #         activity_action=10, activity_change=1)
    #     if pre_10_log is not None:
    #         nowdate = timezone.now().date()
    #         pre10_date = pre_10_log.created.date()
    #         interval_act_time = nowdate - pre10_date
    #         dt24 = datetime.timedelta(hours=24)
    #         t1 = interval_time <= dt24
    #         t2 = interval_act_time == 1
    #         t3 = interval_time > dt24
    #         if interval_time <= dt24:
    #             # 这里怎么简化些呢？
    #             if pre_m10_log is not None:
    #                 pre_m10_date = pre_m10_log.created.date()
    #                 interval_mact_date = nowdate - pre_m10_date
    #                 activity_action = None
    #                 if interval_act_time.days < 1:
    #                     activity_action = None
    #                 elif interval_act_time.days == 1 or interval_mact_date.days == 0:
    #                     activity_action = 10
    #                     activity_change = 1
    #             else:
    #                 if interval_act_time.days < 1:
    #                     activity_action = None
    #                 elif interval_act_time.days == 1:
    #                     activity_action = 10
    #                     activity_change = 1
    #         elif interval_time > dt24:
    #             activity_action = -10
    #             i = interval_time.total_seconds() // (24*3600)
    #             j = interval_time.total_seconds() //3600
    #             k = j //24
    #             activity_change = -2*i

    #     else:
    #         activity_action = 10
    #         activity_change = 1
    #         assert False
    #     # if pre_log is None:
    #     #     return None

    #     # if pre_login_log is None:
    #     #     return None
    #     # else:
    #     #     interval_days = (self.created - pre_login_log.created).days
    #     #     if interval_days == 1:
    #     #         activity_action = 10
    #     #         activity_change = 1
    #     #     elif interval_days >1:
    #     #         activity_action = -10
    #     #         activity_change = -1
    #     if activity_action is None:
    #         return None
    #     self.activity_action = activity_action
    #     self.activity_change = activity_change
    #     self.save()

    #     return self.activity_action

class ProviderPayoff(models.Model):
    '''the record of paying the provider'''
    class Meta:
        verbose_name = "ProviderPayoff"
        verbose_name_plural = "ProviderPayoffs"

    def __str__(self):
        return u'teacher:%s has %d sku worthy:%s ' % (str(self.provider), self.skus.count() , str(self.amount))
    provider = models.ForeignKey(Provider)
    skus = models.ManyToManyField(Sku)
    amount = models.FloatField()
    currency = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __unicode__(self):
        return u'%s' % "[" +str(self.id) + "] " +str(self.noti) + " " + str(self.user)

    STATUS_OF_NOTI = (
        (0, '老师发表了回复'),
        (1, '老师确认了你的课，已经开始备课'),
        (2, '老师已经备课完成！'),
        (3, '还有半个小时'),
        (4, '开始上课！(5分钟)'),
        (5, '换了老师'),
        (6, '抱歉，由于老师的时间安排，课程取消。退款到账户余额'),
        (7, '教案被修改'),
        (8, '学生预订你的课啦！该备课了请确认'),
        (9, '学生取消了课'),
        (10, '学生发表了回复'),
        (11, '超级通知'),
        (12, '老师准备就绪，请注意查收上课链接')
    )

    user = models.ForeignKey(User)
    noti = models.IntegerField(choices=STATUS_OF_NOTI)
    sku = models.ForeignKey(Sku, blank=True, null=True,)
    reply = models.ForeignKey(ReplyToSku, blank=True, null=True,)
    note = models.CharField(blank=True, null=True, max_length=200)
    url = models.URLField(blank=True, null=True,)
    open_time = models.DateTimeField(blank=True, null=True,)
    close_time = models.DateTimeField(blank=True, null=True,)

    STATUS_OF_READ = (
        (0, 'unread'),
        (1, 'read'))
    read = models.IntegerField(choices=STATUS_OF_READ, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class ActLog(models.Model):
    """Model definition for ActLog.
    for recording provider activity log
    """

    # TODO: Define fields here

    class Meta:
        """Meta definition for ActLog."""

        verbose_name = 'ActLog'
        verbose_name_plural = 'ActLogs'

    def __unicode__(self):
        """Unicode representation of ActLog."""
        return u'%s' % str(self.buyer_hp)

    log = models.OneToOneField(Log, on_delete=models.CASCADE)
    buyer_hp = models.IntegerField()
    provider_hp = models.IntegerField(blank=True, null=True)
    provider_active_daily = models.IntegerField(blank=True, null=True)
    provider_active_course = models.IntegerField(blank=True, null=True)
    provider_active_community = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=Log)
    def log_save(sender, instance, created, **kwargs):
        if created:
            actlog = ActLog(
                log=instance,
                buyer_hp=instance.user.buyer.hp,
                provider_active_daily=instance.user.provider.active_daily,
                provider_active_course=instance.user.provider.active_course,
                provider_active_community=instance.user.provider.
                active_community)
            actlog.save()

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super(ActLog, self).save(*args, **kwargs)


#upload path methods:

def provider_avatar_path(instance, filename):
    # TODO 暂未启用
    # file will be uploaded to MEDIA_ROOT/provider_avatars/user_<id>/
    return 'provider_avatars/user_{0}/{1}'.format(instance.user.id, filename)

# TODO 有空时咱们一起进行：
# 默认值、是否必填等有些还需要再调整
# max_length长度有些字段可能不够
# 添加日期、修改日期回头统一给每一个 model 加
# 最后再根据文档过一遍，看看还有哪里有遗漏

# TODO 添加方法（coolgene 将写出文档）


# TEST
class TestModelformFK(models.Model):

    class Meta:
        verbose_name = "TestModelformFK"
        verbose_name_plural = "TestModelformFKs"

    def __str__(self):
        return str(self.status)
    sku = models.OneToOneField(Sku, blank=True, null=True)
    topic = models.ForeignKey(Topic)
    status = models.IntegerField()
