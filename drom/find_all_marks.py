from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

url = 'https://www.drom.ru/catalog/'
driver = webdriver.Chrome()
driver.set_window_size(1200, 800)
driver.set_window_position(0, 0)
driver.get(url)
time.sleep(2)
driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[4]/div[5]/div/span/div').click()
time.sleep(2)
elements = driver.find_elements(By.CLASS_NAME, 'e4ojbx43')
marks = []
links_marks = []

for element in elements:
    marks.append(element.text)
    links_marks.append(element.get_attribute('href'))
driver.quit()

i = 0
for link in links_marks:
    link = link.split('/')
    link = link[-2]
    links_marks[i] = link
    i += 1

print(marks)
print(links_marks)