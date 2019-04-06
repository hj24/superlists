from django.db import models
from django.urls import reverse

# Create your models here.
class List(models.Model):
	
	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

class Item(models.Model):
	# 定义文本字段
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

	def __str__(self):
		return self.text

	class Meta:
		unique_together = ('list', 'text')

