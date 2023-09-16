from bs4 import BeautifulSoup
from enum import Enum, auto
import unittest
import requests

##Offline test for html scraping, does not require selenium

'''
html_text = requests.get()
with open('index.html') as html_file:
    content = html_file.read()
    my_soup = BeautifulSoup(content, 'lxml')
    pictures = my_soup.find_all('img')
    print(pictures)

    for picture in pictures :
        print(picture.src)


    ##course_cards = my_soup.find_all('div', class_= 'card')


def read_individual_course(course):
    prereqs = []
'''
visited_set = None

class Requirement:
    from bs4 import BeautifulSoup

    requirements_array = []
    SubReqType = Enum('SubReqType', ['Courses', 'Units', 'Reqirements'])
    the_html = None
    requirements_head = None
    completed = False
    sub_reqs_to_complete = 0
    sub_reqs = []
    parent_array = None


    def __init__(self,  requirements_html):

        ##self.type = type
        self.requirement_head = requirements_html.find('li')
        ##self.requirements_array =[].append(self.requirement_head, self.requirement_head.next_siblings)
        self.find_sub_reqs(requirements_html)
        self.type = determineType(requirements_html)




    

    def find_sub_reqs(self, req):
        ##for req in self.requirements_array:


        block_head = req.find('li', recursive = True)
        
        sub_reqs = []
        if (block_head is not None):

            
            sub_reqs.append(block_head)
            first_requirement = Requirement(block_head)
          ##  print(block_head.text)
            for thing in block_head.next_siblings:
                sub_reqs.append(thing)
               ## print(thing.text)


            for thing in sub_reqs:
                print (thing.text)

            return

def traverse_html_for_list(html, is_head):


    ##print(html)


    head_ul = html.find('ul', recursive= True)
    head_li = html.find('li', recursive= True)

    if head_ul is None and head_li is None:
        ##print (html.name, html.text)
        ##print(is_head)
        return


    ##Going down
    if head_ul is not None:

        if (head_ul.next_sibling is not None):
            sib = head_ul.next_sibling
            traverse_html_for_list(head_ul.next_sibling, False)
        traverse_html_for_list(head_ul, True)



    if head_li is not None:
        ##if (head_li.next_sibling is not None):
          ##  traverse_html_for_list(head_li.next_sibling, False)



        traverse_html_for_list(head_li, True)
    ##print(html.name, html.text)

def html_trav_wrapper(html):
    global visited_set
    visited_set = set() ##reset visited set

    traverse_html_revised(html, True)

##On first call html is a ul

##Modified dfs for prereq searching
def traverse_html_revised(html, is_head):


    sibling_ul_list = []
    sibling_li_list = []


    ul_child = html.find('ul', recursive= True)
    li_child = html.find('li', recursive= True)

    for thing in html.next_siblings:
        if thing.name == 'ul':
            sibling_ul_list.append(thing)
        if thing.name == 'li':
            sibling_li_list.append(thing)

    for ul in sibling_ul_list:
        traverse_html_revised(ul, False)

    for li in sibling_li_list:
        traverse_html_revised(li, False)

    ##print('sibling ul list:', sibling_ul_list)
    ##print('siling li list:', sibling_li_list)

    if ul_child is None and li_child is None:
        print(html)
        return

    if ul_child is not None and ( ul_child not in  visited_set) :

        visited_set.add(ul_child)
        traverse_html_revised(ul_child, True)

    if li_child is not None and ( li_child not in visited_set):
        visited_set.add(li_child)

        traverse_html_revised(li_child, True)






class ReqType(Enum):
    COURSES = auto()
    UNITS = auto()
    REQUIREMENTS = auto()

def determineType(req_html):
    if req_html.text.__contains__('Complete') or req_html.text.__contains__( 'complete'):
        return ReqType.REQUIREMENTS
    ##if req_html.text.__contains__():
     ##   return ReqType.COURSES
    if req_html.text.__contains__('units of') :
        return ReqType.UNITS

    return ReqType.COURSES

def get_data(source_html) -> list:


    ##Start up beautiful soup and create a dictionary for holding different fields
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

    ##requirements = Requirement(total_pre_reqs)
    ##traverse_html_for_list(total_pre_reqs, True)
    ##traverse_html_revised(total_pre_reqs, True)
    html_trav_wrapper(total_pre_reqs)
    ##find_pre_reqs(soup, total_pre_reqs)
    ##sub_reqs = total_pre_reqs.find_all('li', recursive = False)
    num_required = []


    total_list_eles = total_pre_reqs.find('li', recursive=True).find('li', recursive= True)


   ## for thing in total_list_eles.next_siblings:
       ## print(thing,'\n')

    final_info_map = {
                         "CourseName": "course name",
                         "Units" : "units",
                         "Prereqs": "prereqs",
                         "Coreqs": "coreqs",
                         "Notes": "notes"

                      }



local_html = open('STAT261.html', 'r' )
data = get_data(local_html)
