from sums_api.client import SumsClient

sc = SumsClient()
members = sc.extract_members()

for member in members:
	print(member)

sc.driver.quit()