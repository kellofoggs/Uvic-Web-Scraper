import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import os

driver = webdriver.Edge()
options = webdriver.EdgeOptions()


def get_data(url) -> list:
    browser_options = webdriver.EdgeOptions()
    browser_options.headless = False
    infomap = {}
    driver = webdriver.Edge(browser_options)


    driver.get(url)

    driver.implicitly_wait(10)
    info_array = driver.find_elements(By.CLASS_NAME, 'noBreak')
    ##print()


    ##class ="course-view__label___FPV12"
    for thing in info_array:
        section_name = thing.find_element(By.CLASS_NAME, 'course-view__label___FPV12')
        infomap[section_name.text] = thing
        print(thing.text,'\n')

    print(infomap)
    ##print(element.text)


    driver.quit()

url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses'
data = get_data(url)