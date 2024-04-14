import re
import time

import bs4
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from enum import Enum, auto
import codecs

import os

from selenium.webdriver.support.wait import WebDriverWait

webdrivers = []
counter = 0
# browser_options = webdriver.FirefoxOptions()
# # browser_options = webdriver.EdgeOptions()
# browser_options.headless= False
# browser_options.add_argument('--guest')
#
# # driver = webdriver.Edge(options=browser_options)
# driver = webdriver.Firefox(options=browser_options)
def save_html( raw_html, file_name, directory='./HTML', ):

    global counter


    # file_name = (str(counter))+(".html")
    counter = counter+1
    new_file_path = os.path.join(directory, file_name)
    file = codecs.open(new_file_path, "w", "utf-8")
    file.write(raw_html)
    file.close()




'''
Render html for single url, creates new browser options and driver each time.
Selenium is here as dynamic/javascript sites won't load properly without a browser with a JS environment.
'''
def render_html(url, driver, first=True):

    driver.get(url)

    # if not first:
    #     element = driver.find_element(By.CLASS_NAME, 'course-view__itemTitleAndTranslationButton___36N-_')
    element = (By.CLASS_NAME, 'course-view__itemTitleAndTranslationButton___36N-_')
    element_present = EC.presence_of_element_located(element)
    wait = WebDriverWait(driver, timeout=10)
    wait.until(element_present)
    # element = driver.find_element(By.CLASS_NAME, 'course-view__itemTitleAndTranslationButton___36N-_')
    # locator = (By.TAG_NAME, 'h2')

    ##Wait until noBreak sections appear (sections with content we want)

    print(driver.find_element(By.TAG_NAME, 'h2').text)
    ##Take rendered html_and pass it onto beautiful soup for ability to turn off recursive children search
    soup_understands = driver.page_source
    old_tab = driver.current_window_handle
    assert len(driver.window_handles) == 1

    driver.switch_to.new_window('tab')
    new_tab = driver.current_window_handle

    wait.until(EC.number_of_windows_to_be(2))


    driver.switch_to.window(old_tab)
    driver.close()
    driver.switch_to.window(new_tab)


    return soup_understands


def get_all_class_links():
    global browser_options
    global driver

    all_class_main_page_url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses'
    driver.implicitly_wait(10)

    ##Load page and wait until all buttons are loaded
    driver.get(all_class_main_page_url)
    #
    wait = WebDriverWait(driver, timeout=100)
    # wait_ele = driver.find_element(By.ID, "kuali-catalog-main")
    #
    # wait.until(webdriver.support.expected_conditions.visibility_of(wait_ele))
    program_list = driver.find_element(By.ID, 'kuali-catalog-main').find_elements(By.TAG_NAME, 'li')
    master_class_links_list = []

    for program in program_list:
        # print(program)
        wait.until(EC.element_to_be_clickable(program))
        # wait_for_clickable =
        program.click()
        driver.implicitly_wait(50)
        course_list= program.find_element(By.TAG_NAME, 'ul')
        course_links =  course_list.find_elements(By.TAG_NAME, "a")
        for link_element in course_links:
            master_class_links_list.append(link_element.get_attribute("href"))

    return master_class_links_list


def save_all_links():
    data = get_all_class_links()
    with open("links.txt", "w") as txt_file:
        for line in data:
            txt_file.write((line + "\n"))
        txt_file.close()


def save_all_class_htmls():

    driver = create_web_driver()
    # browser_options = webdriver.EdgeOptions()
    # browser_options.headless = False
    # browser_options.add_argument("--guest")
    #
    # driver = webdriver.Edge(browser_options)

    with open("links.txt") as links_file:

        lines = links_file.readlines()

        for i in range(0, len(lines)):
            link = lines[i]
            research = re.search('Current=.*%20', link)

            # print(l)
            #
            if research is not None:
                # print(line)
                print(research.group())
            # if i == 0 or i == len(lines) -1:
            save_html(render_html(link, driver), research.group())
            # else:
            #     save_html(render_html(link, False), research.group())

            # driver.execute_script("window.sessionStorage.clear()")
            #
            # driver.execute_script("window.localStorage.clear()")
            # driver.delete_all_cookies()

def create_web_driver() :
    browser_options = webdriver.FirefoxOptions()
    # browser_options = webdriver.EdgeOptions()
    browser_options.headless = False
    browser_options.add_argument('--guest')
    driver = webdriver.Edge(options=browser_options)
    webdrivers.append(driver)
    return driver

# url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/r1uCgFTXN?bc=true&bcCurrent=STAT261%20-%20Introduction%20to%20Probability%20and%20Statistics%20II&bcGroup=Statistics%20(STAT)&bcItemType=courses'

##save_html(render_html(url))
# get_all_class_links()
# save_all_links()
save_all_class_htmls()
# save_all_class_htmls()
# driver.get("https://www.uvic.ca/calendar/undergrad/index.php#/courses/HJsvjl1TB?bc=true&bcCurrent=ATWP135%20-%20Academic%20Reading%20and%20Writing&bcGroup=Academic%20and%20Technical%20Writing%20Program%20(ATWP)&bcItemType=courses")
# driver.implicitly_wait(10000000000)
# i = 0
# print(driver.page_source)
# while i < 10000000:
#     i += 1
# save_html(driver.page_source, "a")

