from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

# Create your views here.
"""
render 第三个参数是一个字典，把模板变量的名称映射到值上
dict.get(key, default=None) 如果值不在字典中返回默认值
"""
def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})

def new_list(request):
	"""
	item.objects.create 是创建Item对象的简化方式无需再掉用.save()方法
	"""
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		Item.objects.create(text=request.POST['text'], list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})
	# try:
	# 	item.full_clean()
	# 	item.save()
	# except ValidationError:
	# 	list_.delete()
	# 	error = "You can't have an empty list item"
	# 	return render(request, 'home.html', {"error": error})
	# return redirect(list_)

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ItemForm()
	if request.method == 'POST':
		form = ItemForm(data=request.POST)
		if form.is_valid():
			Item.objects.create(text=request.POST['text'], list=list_)
			return redirect(list_)
	return render(request, 'list.html', {'list': list_, "form": form})


