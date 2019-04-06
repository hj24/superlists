from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
	"""docstring for NewVisitorTest"""
	# def __init__(self, arg):
	# 	super(NewVisitorTest, self).__init__()
	# 	self.arg = arg

	def test_can_start_a_list_for_one_user(self):
		# kobe 听说有个很酷的在线待办事项应用
		# 他去看了这个应用的首页
		self.browser.get(self.live_server_url)
		# 他注意到网页的标题和头部都包含”To-Do“这个词
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text) 
		# 应用邀请他输入一个代办事项
		inputbox = self.get_item_input_box()
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item' 
		)
		# 他在文本框中输入了”Buy peacock feathers“
		inputbox.send_keys('Buy a new basketball')
		# 他按回车以后页面更新了
		# 待办事项中显示了”1：Buy a new basketball“
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy a new basketball')
		# 页面中又显示了一个文本框，可以输入其它代办事项
		# 他又输入了 ”play basketball to win the game“
		inputbox = self.get_item_input_box()
		inputbox.send_keys('play basketball to win the game')
		inputbox.send_keys(Keys.ENTER)
		# 页面再次更新, 他的清单中显示了两个待办事项
		self.wait_for_row_in_list_table('1: Buy a new basketball')
		self.wait_for_row_in_list_table('2: play basketball to win the game')
		# kobe想知道这个网站是否会记住她的清单
		# 他看到网站为他生成了唯一一个URL
		# 页面中有一些文字解说这个功能
		# self.fail('Finish the test!')
		# 他访问那个URL 发现待办事项清单还在
		# 他很满意，训练去了

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# kobe 新建一个待办事项清单
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy a new basketball')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy a new basketball')

		# 他注意到清单有一个唯一的url
		kobe_list_url = self.browser.current_url
		self.assertRegex(kobe_list_url, '/lists/.+')

		# 现在一名叫james的新用户访问了这个网站
		## 我们使用一个新浏览器会话
		## 确保kobe的信息不会从cookie中泄露出去
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# jame 访问了首页
		# 页面中看不到kobe的清单
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy a new basketball', page_text)

		# james输入了一个新的待办事项想，新建一个清单
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy wifi')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy wifi')

		# james获得了他的唯一URL
		james_list_url = self.browser.current_url
		self.assertRegex(james_list_url, '/lists/.+')
		self.assertNotEqual(kobe_list_url, james_list_url)

		# 这个页面还是没有kobe的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy a new basketball', page_text)
		self.assertIn('Buy wifi', page_text)

		# 两人都很满意，去训练了
