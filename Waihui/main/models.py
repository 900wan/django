# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Buyer(models.Model):

    class Meta:
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"

    def __unicode__(self):
        return self.nickname
    user = models.OneToOneField(User)
    nickname = models.CharField(required=True, max_length=50)
    brithday = models.DateField()
    mother_tongue = models.ForeignKey(Language)
    provider = models.ForeignKey(Provider)
    time_zone = models.CharField(, max_length=50)


class Provider(models.Model):

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    def __unicode__(self):
        return self.name
    user = models.OneToOneField(User)
    ROOKIE = 1
    APPLIED = 2
    INTERN = 3
    FORMAL = 4
    LEVELS_OF_TEACHER_CHOICES = (
        (ROOKIE,'非教师'),
        (APPLIED,'已申请'),
        (INTERN,'实习'),
        (FORMAL,'正式'),
    )
    status = models.IntegerField(max_length=2,
        choices='LEVELS_OF_TEACHER_CHOICES', 
        default=ROOKIE)
    name = models.CharField(required=True, max_length=50)
    weekday_pattern = models.CommaSeparatedIntegerField()


class Sku(models.Model):

    class Meta:
        verbose_name = "Sku"
        verbose_name_plural = "Skus"

    def __unicode__(self):
        return "("+u(self.start_time)+")"+self.topic
    provider = models.ForeignKey(Provider, required=True)
    buyer = models.ForeignKey(Buyer)
    
    FORBOOK = 1
    PREBOOKED = 2
    BOOKED = 3
    FINISHED = 4
    STATUES_OF_SKU_CHOICES = (
        (FORBOOK,'可预约'),
        (PREBOOKED,'已预约'),
        (BOOKED,'已定'),
        (FINISHED,'已结束'),
    )
    
    statue = models.IntegerField(
        required=True,
        max_length=2,
        choices='STATUES_OF_SKU_CHOICES',
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    topic = models.ForeignKey(Topic)


class Language(models.Model):

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __unicode__(self):
        return self.english_name
    chinese_name = models.CharField(required=True, max_length=50)
    english_name = models.CharField(required=True, max_length=50)
    local_name = models.CharField(required=True, max_length=50)


class Topic(models.Model):
    
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
    
    def __unicode__(self):
        return self.name
    name = models.CharField(required=True, null=False, max_length=50)
    category = models.ForeignKey(TopicCategory)


class TopicCategory(models.Model):

    class Meta:
        verbose_name = "TopicCategory"
        verbose_name_plural = "TopicCategorys"

    def __unicode__(self):
        return self.name
    name = models.CharField(required=True, max_length=50)
    background_image = models.URLField()


class Wallet(models.Model):

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __unicode__(self):
        return self.cny_balance
    user = models.ForeignKey(User)
    cny_balance = models.FloatField(required=True, default=0)
    display_currency = models.CharField(required=True, default= "cny" , max_length=50)
    

class ReviewTovProvider(models.Model):

    class Meta:
        verbose_name = "ReviewTovProvider"
        verbose_name_plural = "ReviewTovProviders"

    def __unicode__(self):
        return self.score
    from = models.ForeignKey(User)
    to = models.ForeignKey(User)
    sku = models.ForeignKey(Sku)
    questionnaire = models.CharField(required=True, max_length=50)
    comment = models.CharField(max_length=50)
    score = models.FloatField(required=True)


    
