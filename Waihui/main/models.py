# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
import datetime
# from main.act import act_upgrade_hp
# 无法导入acts

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

    def __unicode__(self):
        return u'%s' % self.name
    user = models.OneToOneField(User)
    ROOKIE = 0
    APPLIED = 1
    INTERN = 2
    FORMAL = 3
    LEVELS_OF_TEACHER_CHOICES = (
        (ROOKIE, '非教师'),
        (APPLIED, '已申请'),
        (INTERN, '实习'),
        (FORMAL, '正式'),
        )
    status = models.IntegerField(
        choices=LEVELS_OF_TEACHER_CHOICES,
        default=ROOKIE,
        )
    name = models.CharField(max_length=50, )
    weekday_pattern = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True)
    fee_rate = models.FloatField(default=1)
    hp = models.FloatField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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
        user.last_login
        d1 = datetime.datetime.now()
        d2 = self.modified
        if (d1-d2).days >= 1:
            return "in if"
        return upgrade_hp(self, theset)

    def set_weekday_pattern(self, theset):
        pass


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
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
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

    def __unicode__(self):
        if self.topic is None:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+"no topic")
        else:
            return u'%s' % str(str(self.id)+". ("+self.start_time.strftime("%c")+") "+str(self.topic))
    provider = models.ForeignKey(Provider, )
    buyer = models.ManyToManyField(Buyer, blank=True)

    FORBOOK = 0
    PREBOOKED = 1
    REFUSED = 2
    LOSTED = 3
    BOOKED = 4
    PREPARED = 5
    FORVOTE = 6
    FINISHED = 7

    STATUS_OF_SKU_CHOICES = (
        (FORBOOK, _(u'可预约')),
        (PREBOOKED, '已预约'),
        (REFUSED, '被拒绝扔池子的'),
        (LOSTED, '彻底没人教'),
        (BOOKED, '已定'),
        (PREPARED, '已备课'),
        (FORVOTE, '已结束代评价'),
        (FINISHED, '已彻底结束 '),
    )
    
    status = models.IntegerField(
        choices=STATUS_OF_SKU_CHOICES,
        default=FORBOOK,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    topic = models.ForeignKey(Topic,blank=True,null=True)
    roomlink = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 7
class Plan(models.Model):

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __unicode__(self):
        pass
    sku = models.OneToOneField(Sku ,blank=True, null=True)
    topic = models.ForeignKey(Topic, )
# 给sku：
# 已备课；已上完；
# 给topic：
# 待审核；成功通过；失败待修改
    status = models.IntegerField()
    content = models.TextField()
    assignment = models.TextField(blank=True,null=True)
    slides = models.TextField(blank=True,null=True)
    materiallinks = models.TextField(blank=True,null=True)
    materialhtml = models.TextField(blank=True,null=True)
    voc = models.TextField(blank=True,null=True)
    copy_from = models.ForeignKey('self',blank=True,null=True)
    # summary 写sum我怕出问题
    sumy = models.TextField(blank=True,null=True)
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
    display_currency = models.CharField( default= "CNY" , max_length=50)
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

    class Meta:
        verbose_name = "ReviewTovProvider"
        verbose_name_plural = "ReviewTovProviders"

    def __unicode__(self):
        return u'%s' % self.score
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.OneToOneField(Sku)
    questionnaire = models.CharField( max_length=50)
    comment = models.CharField(max_length=250,blank=True,null=True)
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def get_score(self):
        # questionnaire =
        pass 

# index 10
class ReviewToBuyer(models.Model):

    class Meta:
        verbose_name = "ReviewToBuyer"
        verbose_name_plural = "ReviewToBuyers"

    def __unicode__(self):
        pass
    provider = models.ForeignKey(Provider)
    buyer = models.ForeignKey(Buyer)
    sku = models.OneToOneField(Sku)
    questionnaire = models.CharField( max_length=50,blank=True,null=True)
    comment = models.CharField(max_length=50,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

# index 11
class ReplyToSku(models.Model):

    class Meta:
        verbose_name = "ReplyToSku"
        verbose_name_plural = "ReplyToSkus"

    def __unicode__(self):
        return u'%s' % self.content
    user = models.ForeignKey(User)
    type = models.IntegerField()
    content = models.TextField()
    reply_to = models.ForeignKey('self',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class OrderType(models.Model):

    class Meta:
        verbose_name = "OrderType"
        verbose_name_plural = "OrderTypes"

    def __str__(self):
        pass
    type = models.CharField( max_length=50)

class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        pass
    buyer = models.ForeignKey(Buyer)
    provider = models.ForeignKey(Provider, null=True)
    cny_price = models.FloatField()
    cny_paid = models.FloatField(default=0)
    pay_method = models.CharField(blank=True, null=True, max_length=50)
    skus = models.ForeignKey(Sku, blank=True, null=True)
    type = models.ForeignKey(OrderType)
# 不可支付、未支付、已支付、已完成、申请退款、已退款……
    UA = 0
    UNPAID = 1
    PAID = 2
    FINISHED = 3
    FORREFUND = 4
    BEREFUND = 5
    STATUS_OF_ORDER_TYPE = (
        (UA, '不可支付'),
        (UNPAID, '未支付'),
        (PAID, '已支付'),
        (FINISHED, '已完成'),
        (FORREFUND, '申请退款'),
        (BEREFUND, '已退款'))

    status = models.IntegerField(
        choices=STATUS_OF_ORDER_TYPE,
        default=UNPAID)

    def upgrade_status(self, theset):
        """对order状态进行升级"""
        self.status = theset
        self.save()


class Log(models.Model):
    '''Model Log is for record of the journal of a User daily action.
    To record this info, your should insert log attribution in Front'''
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        pass
    HTML = 0
    WAP = 1
    IOSAPP = 2
    ANDAPP = 3
    TYPE_OF_CLIENT = (
        (HTML, '网页端'),
        (WAP, '移动网页端'),
        (IOSAPP, 'IOS客户端'),
        (ANDAPP, '安卓客户端'))
    source = models.IntegerField(
        choices=TYPE_OF_CLIENT,
        default=HTML)

    LOGIN = 0
    LOGOUT = 1
    ORDERED = 2
    MODIFIED = 3
    CANCLE = 4
    TYPE_OF_ACTION = (
        (LOGIN, '登陆'),
        (LOGOUT, '登出'),
        (ORDERED, '下单'),
        (MODIFIED, '修改'),
        (CANCLE, '取消'))
    type = models.IntegerField(choices=TYPE_OF_ACTION)
    user = models.OneToOneField(User)

    BUYER = 0
    PROVIDER = 1
    TYPE_OF_CHARACTER = (
        (BUYER, 'buyer'),
        (PROVIDER, 'provider'))
    character = models.IntegerField(choices=TYPE_OF_CHARACTER)
    Dtime = models.DateTimeField(auto_now_add=True)

# TODO 有空时咱们一起进行：
# 默认值、是否必填等有些还需要再调整
# max_length长度有些字段可能不够
# 添加日期、修改日期回头统一给每一个 model 加
# 最后再根据文档过一遍，看看还有哪里有遗漏

# TODO 添加方法（coolgene 将写出文档）
    
