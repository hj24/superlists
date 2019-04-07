import time
from .base import *
from unittest import skip
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class ItemValidationTest(FunctionalTest):

	def wait_for(self, fn):
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)	

	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')

	def test_cannot_add_empty_list_items(self):
		# kobe访问首页，不小心提交了一个空待办事项
		# 输入框中没输入内容他就按下了回车
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# 浏览器截获了请求
		# 清单页面不会加载
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# 他在待办事项中输入了一些文字
		# 错误又消失了
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))

		# 现在能提交了
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# 他有点调皮，又提交了一个空待办事项
		self.get_item_input_box().send_keys(Keys.ENTER)

		# 浏览器这次也不会放行
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# 输入文字之后就没问题了
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		# kobe访问首页，新建一个清单
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wellies')

		# 他不小心输入了一个重复的待办事项
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# 他看到一条有帮助的错误消息
		self.wait_for(lambda: self.assertEqual(
			self.get_error_element().text,
			"You've already got this in your list"
		))


	def test_error_messages_are_cleared_on_input(self):
		# kobe 新建了一个清单，但方法不当，所以出现了一个验证错误
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Bather too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('1: Bather too thick')
		self.get_item_input_box().send_keys('Bather too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertTrue(
			self.get_error_element().is_displayed()
		))

		# 为了消除错误，他开始在输入框中输入内容
		self.get_item_input_box().send_keys('a')

		# 他看到错误消失了，很高兴
		self.wait_for(lambda: self.assertFalse(
			self.get_error_element().is_displayed()
		))





