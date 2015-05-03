# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Buyder(models.Model):

	class Meta:
		verbose_name = "Buyder"
		verbose_name_plural = "Buyders"

	def __str__(self):
		pass
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

	def __str__(self):
		pass
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

    def __str__(self):
        pass
    provider = models.ForeignKey(Provider, required=True)
    buyder = models.ForeignKey(Buyder)
    FORDATE = 1
    HASDATE = 2
    HASDEAL = 3
    HASOVER = 4
    STATUES_OF_SKU_CHOICES = (
    	(FORDATE,'可预约'),
    	(HASDATE,'已预约'),
    	(HASDEAL,'已定'),
    	(HASOVER,'已结束'),
    )
    statue = models.IntegerField(required=True,
    	max_length=2,
    	choices='STATUES_OF_SKU_CHOICES',
    )
    	start_time = models.DateTimeField()
    	end_time = models.DateTimeField()
    	topic = models.ForeignKey(Topic)

