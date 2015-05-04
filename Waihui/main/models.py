# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Buyer(models.Model):

	class Meta:
		verbose_name = "Buyer"
		verbose_name_plural = "Buyers"

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
	statue = models.IntegerField(required=True,
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

	def __str__(self):
		pass
	english_name = models.CharField(required=True, max_length=50)
	