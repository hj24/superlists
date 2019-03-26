from django.db import models

# Create your models here.
class Item(models.Model):
	# 定义文本字段
	text = models.TextField(default='')