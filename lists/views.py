from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	"""
	render 第三个参数是一个字典，把模板变量的名称映射到值上
	dict.get(key, default=None) 如果值不在字典中返回默认值
	"""
	return render(request, 'home.html', {
		'new_item_text': request.POST.get('item_text', ''),
	})
