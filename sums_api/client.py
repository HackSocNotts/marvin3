from config import SELENIUM_URL, SUMS_USERNAME, SUMS_PASSWORD, SUMS_GROUP_ID

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

from sums_api.member import Member

class SumsClient:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		#options.add_argument("--no-sandbox")
		#options.add_argument("--disable-dev-shm-usage")

		self.driver = webdriver.Remote(
			command_executor=SELENIUM_URL,
			options=options,
		)
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

		self.wait.until(
			EC.url_contains("idp.nottingham.ac.uk")
		)

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
			EC.url_contains("https://su.nottingham.ac.uk/")
		)

	def navigate_to_student_dashboard(self):
		# self.driver.get(f"https://student-dashboard.sums.digital/")
		# the dashboard link sends you with a secret in the URL so you can't just go direct to dashboard
		self.wait.until(
			EC.element_to_be_clickable(
				(By.ID, "userActionsInvoker")
			)
		).click()

		self.wait.until(
			EC.element_to_be_clickable(
				(By.ID, "studentDashboardLink")
			)
		).click()

		self.wait.until(
			EC.visibility_of_element_located(
				(By.ID, "total-spent-card") # any id that'll be visible once the log in succeeds
			)
		)

	def navigate_to_members_table(self):
		self.driver.get(f"https://student-dashboard.sums.digital/groups/{SUMS_GROUP_ID}/members")

		self.wait.until(
			EC.visibility_of_element_located(
				(By.ID, "group-member-list-datatable")
			)
		)

	def add_large_select_value(self):
		self.driver.execute_script("""
			const select = document.querySelector(
				"#group-member-list-datatable_length select"
			);
			const option = document.createElement("option");
			option.value = "100000";
			option.text = "100000";

			select.appendChild(option);
		""")

	def show_all_members(self):
		select = self.wait.until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, "#group-member-list-datatable_length select")
			)
		)

		self.add_large_select_value()
		Select(select).select_by_value("100000")


	def extract_members_from_table(self):
		table = self.wait.until(
			EC.visibility_of_element_located(
				(By.ID, "group-member-list-datatable")
			)
		)

		rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
		members = []

		for row in rows:
			cells = row.find_elements(By.TAG_NAME, "td")

			if not cells:
				continue

			members.append(
				Member(
					student_id=cells[0].text.strip(),
					join_date=date.fromisoformat(
						cells[4].get_attribute("textContent").strip()
					),
				)
			)

		return members

	def auth(self):
		self.navigate_to_idp_login()
		self.submit_login_form()

	def goto_members_table(self):
		self.navigate_to_student_dashboard()
		self.navigate_to_members_table()
		self.show_all_members()
	
	def extract_members(self):
		self.auth()
		self.goto_members_table()
		members = self.extract_members_from_table()
		return members