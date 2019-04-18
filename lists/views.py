from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm, ExistingListItemForm

from django.contrib.auth import get_user_model
User = get_user_model()

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
		list_ = List()
		list_.owner = request.user
		list_.save()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)
	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(request, 'list.html', {'list': list_, "form": form})

def my_lists(request, email):
	owner = User.objects.get(email=email)
	return render(request, 'my_lists.html', {'owner': owner})


