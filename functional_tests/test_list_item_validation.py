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

		# 首页刷新了，显示一个错误消息
		# 提示待办事项不能为空
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# 他输入一些文字，然后再次提交，这次没问题了
		inputbox = self.get_item_input_box()
		inputbox.send_keys('play basketball to win the game')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: play basketball to win the game')

		# 他有点调皮，又提交了一个空待办事项
		self.get_item_input_box().send_keys(Keys.ENTER)

		# 在清单页面他看到了一个类似的错误
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# 输入文字之后就没问题了
		inputbox = self.get_item_input_box()
		inputbox.send_keys('buy a new basketball')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: play basketball to win the game')
		self.wait_for_row_in_list_table('2: buy a new basketball')







