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







