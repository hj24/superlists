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

	def test_only_saves_items_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)

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

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')

	def test_display_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')





