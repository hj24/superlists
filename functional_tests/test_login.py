from django.core import mail
from selenium.webdriver.common.keys import Keys
import re, time
import os, poplib
from .base import *

#TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

	def wait_for_email(self, test_email, subject):
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body
		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com')
		try:
			inbox.user(test_email)
			inbox.pass_(os.environ['GMAIL_PASSWORD'])
			while time.time() - start < 60:
				# 获取最新的 10 封邮件
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting msg', i)
					_, lines, _ = inbox.retr(i)
					lines = [l.decode('utf8') for l in lines]
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()

	def test_can_get_email_link_to_log_in(self):
		# kobe注意到这个的清单网站
		# 第一次保存时注意到导航栏有个登录选项
		# 看到要求输入电子邮件，她便输入了
		if self.staging_server:
			test_email = 'developer.mamba@gmail.com'
		else:
			test_email = 'edith@example.com'

		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

		# 出现一条信息告诉他邮件已发出
		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
		))

		# 他查看邮箱，看到一条信息
		body = self.wait_for_email(test_email, SUBJECT)

		# 邮箱中有个链接
		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.+$', body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)
		
		# 他点击了链接
		self.browser.get(url)

		# 他登陆了
		self.wait_to_be_logged_in(email=test_email)

		# 他退出了
		self.browser.find_element_by_link_text('Log out').click()

		# 他退出了
		self.wait_to_be_logged_out(email=test_email)


