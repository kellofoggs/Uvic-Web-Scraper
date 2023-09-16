import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from enum import Enum, auto
import codecs


import os

from selenium.webdriver.support.wait import WebDriverWait



driver = webdriver.Edge()
##options = webdriver.EdgeOptions()
wait = WebDriverWait(driver, timeout = 30)
'''
def get_data(url) -> list:
    browser_options = webdriver.EdgeOptions()
    browser_options.headless = False
    infomap = {}
    driver = webdriver.Edge(browser_options)


    driver.get(url)
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'noBreak'))
    WebDriverWait(driver, timeout = 10).until(element_present)

  ##  wanted_component = driver.find_element(By.CLASS_NAME, 'noBreak')

    ##wanted_component.send_keys("Displayed")

    ##Wait for desired elements to load then put them into a map
    ##driver.implicitly_wait(10)
    page_html = driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML')
    soup = BeautifulSoup(page_html, 'lxml')

    print(soup.text)

    info_array = soup.find_all('div.noBreak')

    ##class ="course-view__label___FPV12"
    for thing in info_array:
        section_name = thing.find('.course-view__label___FPV12').text
        print(thing.text)
        infomap[section_name] = thing

        ##print(thing.text,'\n')
    print(infomap)
    ##prereqs_list = infomap["Prerequisites"].find('ul').text
    ##print(prereqs_list)


    
    
    for thing in prereqs_list:
        print(thing.text, '\n')
    
    ##print(prereqs_list)

    ##print(infomap)

    prereqs = []

    ##print(element.text)


    driver.quit()
    return info_array

url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses'
data = get_data(url)


'''

def save_html(d):
    new_file = os.path.join("D:\pythonProject", "STAT261.html")
    file = codecs.open(new_file,"w", "utf-8")
    h = d
    file.write(h)
    file.close()

def get_data(source_html) -> list:


    soup = BeautifulSoup(source_html, 'lxml')
    infomap = {}





    ##Wait for desired elements to load then put them into a map

    info_array = soup.find_all('div', class_ = 'noBreak')

    ##class ="course-view__label___FPV12"
    for thing in info_array:
        section_name = thing.find(class_ ='course-view__label___FPV12').text
        infomap[section_name] = thing
        ##print(thing,'\n')

    ##print(infomap)


    total_pre_reqs = infomap["Prerequisites"].find('ul', recursive = True)

    ##find_pre_reqs(soup, total_pre_reqs)
    sub_reqs = total_pre_reqs.find_all('li', recursive = False)
    num_required = []



    final_info_map = {
                         "CourseName": "course name",
                         "Units" : "units",
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

def gather_pre_reqs_wrapper(soup, pre_req_block):
    req_array = []
    for requirement_html in pre_req_block:


        requirement = Requirement(requirement_html)
        req_array.append(requirement)


        find_pre_reqs(soup, requirement_html)






##Treating the html as a tree we find the height of the prereq subtree
def find_level(soup, pre_req_block, level):



    if (pre_req_block.find_all('ul') is not None):
        parent_list = pre_req_block.find_all('ul')
        children_list = pre_req_block.find_all('ul')



class Requirement:

    requirements_array = []
    SubReqType = Enum('SubReqType', ['Courses', 'Units', 'Reqirements'])
    requirements_head = None
    completed = False
    sub_reqs_to_complete = 0
    sub_reqs = []
    parent_array = None


    def __init__(self, type, requirements_html, parent_array):

        ##self.type = type
        self.requirement_head = requirements_html.find('li')
        self.requirements_array =[].append(self.requirement_head, self.requirement_head.next_siblings)
        self.find_sub_reqs()





    def find_sub_reqs(requirement):
        ##for req in self.requirements_array:


        block_head = requirement.find('li', recursive = True)

        sub_reqs = []
        sub_reqs.append(block_head)
        if (block_head is not None):
            first_requirement = Requirement(block_head)

            for thing in block_head.next_siblings:
                sub_reqs.append(thing)


            return


class ReqType(Enum):
    COURSES = auto()
    UNITS = auto()
    REQUIREMENTS = auto()

def determineType(requirement_html):
    if requirement_html.text.__contains__('Complete', 'complete'):
        return ReqType.REQUIREMENTS
    if requirement_html.text.__contains__():
        return ReqType.COURSES
    if requirement_html.text.__contains__('units of') :
        return ReqType.UNITS





def render_html(url):
    browser_options = webdriver.EdgeOptions()
    browser_options.headless = False
    driver = webdriver.Edge(browser_options)

    driver.get(url)
    ##Wait until noBreak sections appear (sections with content we want)
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'noBreak'))
    WebDriverWait(driver, timeout=10).until(element_present)
    ##  wanted_component = driver.find_element(By.CLASS_NAME, 'noBreak')

    ##Take rendered html_and pass it onto beautiful soup for ability to turn off recursive children search
    ##print(driver.page_source)
    soup_understands = driver.page_source
    return soup_understands


##url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses '
url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/r1uCgFTXN?bc=true&bcCurrent=STAT261%20-%20Introduction%20to%20Probability%20and%20Statistics%20II&bcGroup=Statistics%20(STAT)&bcItemType=courses'
local_html = open('STAT261.html', 'r' )
data = get_data(local_html)






