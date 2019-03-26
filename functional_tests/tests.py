from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
	"""docstring for NewVisitorTest"""
	# def __init__(self, arg):
	# 	super(NewVisitorTest, self).__init__()
	# 	self.arg = arg

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# kobe 听说有个很酷的在线待办事项应用
		# 他去看了这个应用的首页
		self.browser.get(self.live_server_url)
		# 他注意到网页的标题和头部都包含”To-Do“这个词
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text) 
		# 应用邀请他输入一个代办事项
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item' 
		)
		# 他在文本框中输入了”Buy peacock feathers“
		inputbox.send_keys('Buy a new basketball')
		# 他按回车以后页面更新了
		# 待办事项中显示了”1：Buy a new basketball“
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy a new basketball')
		# 页面中又显示了一个文本框，可以输入其它代办事项
		# 他又输入了 ”play basketball to win the game“
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('play basketball to win the game')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		# 页面再次更新, 他的清单中显示了两个待办事项
		self.check_for_row_in_list_table('1: Buy a new basketball')
		self.check_for_row_in_list_table('2: play basketball to win the game')
		# kobe想知道这个网站是否会记住她的清单
		# 他看到网站为他生成了唯一一个URL
		# 页面中有一些文字解说这个功能
		self.fail('Finish the test!')

