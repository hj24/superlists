from django.test import TestCase
from django.urls import resolve
from lists.views import home_page	# 自定义的视图函数
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from unittest import skip
from lists.forms import (
	DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
	ExistingListItemForm, ItemForm
)

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

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		# 检查表单是否属于正确的类
		self.assertIsInstance(response.context['form'], ItemForm)

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
			data={'text': 'A new item for an existing list'}
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
			data={'text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, f'/lists/{correct_list.id}/')

	def post_invalid_input(self):
		list_ = List.objects.create()
		return self.client.post(
			f'/lists/{list_.id}/',
			data={'text': ''}
		)

	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Item.objects.count(), 0)

	def test_for_invalid_input_renders_list_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ExistingListItemForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	
	def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='textey')
		response = self.client.post(
			f'/lists/{list1.id}/',
			data={'text': 'textey'}
		)
		excepted_error = escape(DUPLICATE_ITEM_ERROR)
		self.assertContains(response, excepted_error)
		self.assertTemplateUsed(response, 'list.html')
		self.assertEqual(Item.objects.all().count(), 1)

	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, 'name="text"')

class NewListTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(f'/lists/new', data={'text': 'A new list item'})
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		
	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)

class MyListsTest(TestCase):

	def test_my_lists_url_renders_my_lists_template(self):
		response = self.client.get('/lists/users/a@b.com')
		self.assertTemplateUsed(response, 'my_lists.html')





