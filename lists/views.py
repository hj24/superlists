from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
"""
render 第三个参数是一个字典，把模板变量的名称映射到值上
dict.get(key, default=None) 如果值不在字典中返回默认值
"""
def home_page(request):
	return render(request, 'home.html')

def new_list(request):
	"""
	item.objects.create 是创建Item对象的简化方式无需再掉用.save()方法
	"""
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect(f'/lists/{list_.id}/')

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': list_})


