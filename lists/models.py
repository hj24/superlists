from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class List(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
	
	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

	@staticmethod
	def create_new(first_item_text, owner=None):
		list_ = List.objects.create(owner=owner)
		Item.objects.create(text=first_item_text, list=list_)
		return list_

	@property
	def name(self):
		return self.item_set.first().text
	

class Item(models.Model):
	# 定义文本字段
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')



