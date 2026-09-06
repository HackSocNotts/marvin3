from sums_api.client import SumsClient

sc = SumsClient()
sc.auth()

input("close")

sc.driver.quit()