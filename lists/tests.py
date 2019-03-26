from django.test import TestCase
from django.urls import resolve
from lists.views import home_page	# 自定义的视图函数
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

	# def test_root_url_resolves_to_home_page_view(self):
	# 	found = resolve("/")
	# 	self.assertEqual(found.func, home_page)
	# 测试是否正确渲染模板的一种方法 render_to_string
	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	html = response.content.decode('utf8')
	# 	excepted_html = render_to_string('home.html')
	# 	self.assertEqual(html, excepted_html)
	# 测试是否正确渲染模板的另一种方法 TestClient
	def test_home_page_returns_correct_html(self):
		# 隐式测试test_root_url_resolves_to_home_page_view
		response = self.client.get('/')		
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first(ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first(ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')


