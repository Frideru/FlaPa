from selenium import webdriver
 
driver = webdriver.Chrome()
driver.get("https://www.lambdatest.com")
email_form = driver.find_element_by_id("testing_form")
