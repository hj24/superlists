from django.core import mail
from selenium.webdriver.common.keys import Keys
import re, time

from .base import *

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

	# def wait_for(self, fn):
	# 	start_time = time.time()
	# 	while True:
	# 		try:
	# 			return fn()
	# 		except (AssertionError, WebDriverException) as e:
	# 			if time.time() - start_time > MAX_WAIT:
	# 				raise e
	# 			time.sleep(0.5)	

	def test_can_get_email_link_to_log_in(self):
		# kobe注意到这个的清单网站
		# 第一次保存时注意到导航栏有个登录选项
		# 看到要求输入电子邮件，她便输入了
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		# 出现一条信息告诉他邮件已发出
		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
		))

		# 他查看邮箱，看到一条信息
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		# 邮箱中有个链接
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{email.body}')
		url = url_search.group(0)
		print(self.live_server_url, url)
		self.assertIn(self.live_server_url, url)
		print(url)
		# 他点击了链接
		self.browser.get(url)

		# 他登陆了
		# self.wait_for(
		# 	lambda: self.browser.find_element_by_link_text('Log out')
		# )
		# navbar = self.browser.find_element_by_css_selector('.navbar')
		# self.assertIn(TEST_EMAIL, navbar.text)
		self.wait_to_be_logged_in(email=TEST_EMAIL)

		# 他退出了
		self.browser.find_element_by_link_text('Log out').click()

		# 他退出了
		# self.wait_for(
		# 	lambda: self.browser.find_element_by_name('email')
		# )
		# navbar = self.browser.find_element_by_css_selector('.navbar')
		# self.assertNotIn(TEST_EMAIL, navbar.text)
		self.wait_to_be_logged_out(email=TEST_EMAIL)


