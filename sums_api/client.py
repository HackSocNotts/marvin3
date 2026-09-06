from config import SUMS_USERNAME, SUMS_PASSWORD

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SumsClient:
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.wait = WebDriverWait(self.driver, 10)

	def navigate_to_idp_login(self):
		# brittle ul/li navigation fortunately now redundant because the login button just takes you here 
		self.driver.get("https://su.nottingham.ac.uk/sign-in/sso")

		# self.wait.until(
		# 	EC.element_to_be_clickable(
		# 		(By.ID, "userActionsInvoker")
		# 	)
		# ).click()

		# # clicks profile icon in top right, then "student dashboard"
		# self.wait.until(
		# 	EC.element_to_be_clickable(
		# 		(By.XPATH, '//*[@id="userActions"]/ul/li[1]/a[1]')
		# 	)
		# ).click()

		# self.wait.until(
		# 	EC.url_contains("idp.nottingham.ac.uk")
		# )

	def submit_login_form(self):
		username = self.wait.until(
			EC.visibility_of_element_located(
				(By.ID, "username")
			)
		)
		username.send_keys(SUMS_USERNAME)

		password = self.wait.until(
			EC.visibility_of_element_located(
				(By.ID, "password")
			)
		)
		password.send_keys(SUMS_PASSWORD)

		self.driver.find_element(
			By.CSS_SELECTOR,
			"button[type='submit']"
		).click()

		self.wait.until(
			EC.url_contains("student-dashboard.sums.su")
		)

	#def navigate_to_student_dashboard()


	def auth(self):
		self.navigate_to_idp_login()
		self.submit_login_form()


