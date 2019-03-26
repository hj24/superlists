from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
	"""docstring for NewVisitorTest"""
	# def __init__(self, arg):
	# 	super(NewVisitorTest, self).__init__()
	# 	self.arg = arg

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# kobe 听说有个很酷的在线待办事项应用
		# 他去看了这个应用的首页
		self.browser.get('http://localhost:8000')
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
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy a new basketball' for row in rows),
			"New to-do item did not appear in table"
		)
		# 页面中又显示了一个文本框，可以输入其它代办事项
		# 他又输入了 ”play basketball to win the game“
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')