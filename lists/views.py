from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
"""
render 第三个参数是一个字典，把模板变量的名称映射到值上
dict.get(key, default=None) 如果值不在字典中返回默认值
"""
def home_page(request):
	"""
	item.objects.create 是创建Item对象的简化方式无需再掉用.save()方法
	"""
	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)
		return redirect('/lists/the-only-list-in-the-world/')
	return render(request, 'home.html')

def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})
