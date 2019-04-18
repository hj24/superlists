from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

	def creat_pre_authenticated_session(self, email):
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)
		## 为了设定cookie
		## 而404页面是加载最快的
		## 这种做法仅仅在使用LiveServerTestCase时才有效
		self.browser.get(self.live_server_url + '/404_no_such_url/')
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/',
		))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		# kobe 已经是登录用户
		self.creat_pre_authenticated_session('edith@example.com')

		# 他访问清单，新建了一个清单
		self.browser.get(self.live_server_url)
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		# 他第一次看到My Lists链接
		self.browser.find_element_by_link_text('My lists').click()

		# 他看到这个页面中有他创建的清单
		# 而且清单根据第一个待办事项命名
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
		)
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)

		# 他决定再建一个清单试试
		self.browser.get(self.live_server_url)
		self.add_list_item('Click cows')
		second_list_url = self.browser.current_url

		# 在My lists页面，这个新建的清单也显示出来了
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Click cows')
		)
		self.browser.find_element_by_link_text('Click cows').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
		)

		# 他退出后，	My lists链接不见了
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_link_text('My lists'),
			[]
		))

