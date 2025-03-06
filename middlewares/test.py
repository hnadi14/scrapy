from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.add_argument("--headless")
edge_service = EdgeService(executable_path=r"C:\Users\hn\Downloads\msgd\msedgedriver.exe")
driver = webdriver.Edge(service=edge_service, options=edge_options)

driver.get("https://www.aparat.com/")
print(driver.title)  # چاپ عنوان صفحه
driver.quit()