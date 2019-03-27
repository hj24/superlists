from django.db import models

# Create your models here.
class List(models.Model):
	pass

class Item(models.Model):
	# 定义文本字段
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

