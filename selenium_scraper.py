import bs4
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from enum import Enum, auto
import codecs

import os

from selenium.webdriver.support.wait import WebDriverWait
counter = 0
##driver = webdriver.Edge()
##options = webdriver.EdgeOptions()
##wait = WebDriverWait(driver, timeout=30)



def save_html(raw_html):

    ##file_name = raw_html.find(By.CLASS_NAME, "course-view__itemTitleAndTranslationButton___36N-_").text + (".html")
    global counter


    file_name = (str(counter))+(".html")
    counter = counter+1
    new_file = os.path.join(".", file_name)
    file = codecs.open(new_file, "w", "utf-8")
    file.write(raw_html)
    file.close()


def get_data(source_html) -> list:
    soup = BeautifulSoup(source_html, 'lxml')
    infomap = {}

    ##Wait for desired elements to load then put them into a map

    info_array = soup.find_all('div', class_='noBreak')

    ##class ="course-view__label___FPV12"
    for thing in info_array:
        section_name = thing.find(class_='course-view__label___FPV12').text
        infomap[section_name] = thing
        ##print(thing,'\n')

    ##print(infomap)

    total_pre_reqs = infomap["Prerequisites"].find('ul', recursive=True)

    ##find_pre_reqs(soup, total_pre_reqs)
    sub_reqs = total_pre_reqs.find_all('li', recursive=False)
    num_required = []

    final_info_map = {
        "CourseName": "course name",
        "Units": "units",
        "Prereqs": "prereqs",
        "Coreqs": "coreqs",
        "Notes": "notes"

    }

    '''
    ##print(infomap)

    prereqs = []

    ##print(element.text)


    driver.quit()
    return info_array
    '''




def render_html(url):
    browser_options = webdriver.EdgeOptions()
    browser_options.headless = False
    driver = webdriver.Edge(browser_options)

    driver.get(url)
    ##Wait until noBreak sections appear (sections with content we want)
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'noBreak'))
    WebDriverWait(driver, timeout=10000).until(element_present)
    ##  wanted_component = driver.find_element(By.CLASS_NAME, 'noBreak')
    # print(driver.find_element(By.CLASS_NAME, "course-view__itemTitleAndTranslationButton___36N-_").text)

    ##Take rendered html_and pass it onto beautiful soup for ability to turn off recursive children search
    ##print(driver.page_source)
    soup_understands = driver.page_source
    return soup_understands


def get_all_class_links():
    ##keep in selenium so webpage still interactable
    browser_options = webdriver.EdgeOptions()
    # browser_options.add_argument("--headless=new")

    # browser_options.headless = True

    driver = webdriver.Edge(browser_options)

    all_class_main_page_url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses'

    ##Load page and wait until all buttons are loaded
    driver.get(all_class_main_page_url)
    driver.implicitly_wait(10)
    ##element_present = EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    ##WebDriverWait(driver,timeout=10).until(element_present)


    program_list = driver.find_element(By.CLASS_NAME, 'style__groups___NnCy6').find_elements(By.TAG_NAME, 'li')
    master_class_links_list = []
    for program in program_list:


        program.click()
        driver.implicitly_wait(2)
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
   ## links_file = open("links.txt")

    with open("links.txt") as links_file:

        for line in links_file:
            save_html(render_html(line))

##url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses '
url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/r1uCgFTXN?bc=true&bcCurrent=STAT261%20-%20Introduction%20to%20Probability%20and%20Statistics%20II&bcGroup=Statistics%20(STAT)&bcItemType=courses'
'''
local_html = open('STAT261.html', 'r' )
data = get_data(local_html)
'''
##save_html(render_html(url))
#get_all_class_links()
# save_all_links()
# save_all_class_htmls()
