from django.test import TestCase
from django.urls import resolve
from lists.views import home_page	# 自定义的视图函数
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape

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

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		# response.context[] 表示要传入render函数的上下文
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, f'/lists/{correct_list.id}/')


class NewListTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(f'/lists/new', data={'item_text': 'A new list item'})
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		# print(response.content.decode())
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)





