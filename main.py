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

# Set for DFS that is reinitialized whenever wrapper is called
visited_set = None

# Class for requirements. A requirement could be a singular class, a certain amount of units or a collection of the other 2
class Requirement:
    type = None
    course_title = None
    course_description = None
    name = None
    sub_reqs = None
    quantity = 0
    html = None
    my_map = {}
    sub_maps = []

    def __init__(self, doc):
        self.type = determineType(doc)
        self.name = doc.text
        self.html = doc

        if self.type == ReqType.REQUIREMENTS:
            self.prep_for_reqs()
        elif self.type == ReqType.COURSES:
            self.prep_for_courses()

        elif self.type == ReqType.UNITS:
            self.prep_for_units


        if self.sub_reqs is not None and len(self.sub_reqs) > 0:
            for req in self.sub_reqs:
                self.sub_maps.append(req.return_info())
                print(req.name)


        self.my_map = {
            'type': self.type,
            'name': self.name,
            'course_title': self.course_description,
            'sub reqs': self.sub_maps,
            'quantity': self.quantity
        }
        ##print(self)
        return

    def get_map_version(self):
        return self.my_map

    def prep_for_courses(self):
        hyphen_location = None
        found_title = False


        ##if self.type == ReqType.COURSES:
        course_long = []
        string_number_array = []
        link = self.html.find('a')
        if link is not None:
            self.name = link.text

        ##found_hyphen = False
        for i in range(0, len(self.html.text)):
            char = self.html.text[i]
            ##When we find char we can start looking at text after it
            if char == '-':
                ##found_hyphen = True
                hyphen_location = i
                break

        for j in range(hyphen_location + 2, len(self.html.text)):
            char = self.html.text[j]
            course_long.append(char)

            if not found_title:
                if char == '(':
                    course_long.pop(len(course_long) - 1)

                    ##print(''.join(course_long))
                    self.course_title = ''.join(course_long)
                found_title = True
                ##If we found the '(' before the number then we can go further into the string to look for the credit amount
                continue

            ##Find the credits that the course has
            if found_title:
                if ord(char) in range(48, 57) or ord(char) == 46:
                    string_number_array.append(char)
                elif ord(char) == 41:
                    to_be_converted_to_int = ''.join(string_number_array)
                    self.quantity = float(to_be_converted_to_int)
                    return

    def prep_for_reqs(self):
        self.name = "Complete"
        return

    def prep_for_units(self):
        return 0

    def get_html(self):
        return self.html

    def print_info(self):
        my_info = self.return_info()

        print(my_info)
        print(self.html.text)

    def return_info(self):
        my_info = {
            'type': self.type,
            'name': self.name,
            'course_title': self.course_description,
            'sub reqs': self.sub_reqs,
            'quantity': self.quantity

        }

        return my_info

    def extrapolate_from_text(self):

        ##C->O->M->P->L->E->T->E
        dfa = [

        ]

    def add_to_sub_reqs(self, element):
        self.sub_reqs.append(element)

    def set_sub_reqs(self, in_array):
        self.sub_reqs = in_array

    def clean_up_quantity(self, input):
        if self.type == ReqType.REQUIREMENTS:
            self.sub_reqs = []
            quantity = int(self.html.find('span').text)

        if self.type == ReqType.COURSES:
            quantity = int(self.html.find(
                'span').text)  ##get the span element then get its text then remove the last 5 characters and remove parantheses


class ReqType(Enum):
    REQUIREMENTS = auto()
    COURSES = auto()
    UNITS = auto()


def determineType(requirement_html):
    if requirement_html.text.__contains__('Complete', 'complete'):
        return ReqType.REQUIREMENTS
    if requirement_html.text.__contains__('units of'):
        return ReqType.UNITS
    return ReqType.COURSES


def find_sub_reqs_wrapper(html):
    global visited_set
    visited_set = set()  ##reset visited set

    req = find_sub_reqs_recursive_revised(html, False)
    ##req.print_info()
    return req


##On first call html is a ul

##Modified dfs for prereq searching
##Returns a requirement object that holds arrays of other requirements under neath it and so on
def find_sub_reqs_recursive_revised(html, is_head):
    sibling_li_list = []
    sibling_req = []
    child_req_array = []

    li_child = html.find('li', recursive=True)
    for thing in html.next_siblings:
        if thing.name == 'li':
            sibling_li_list.append(thing)

    for li in sibling_li_list:
        if li not in visited_set:
            thing_two = find_sub_reqs_recursive_revised(li, False)
            sibling_req.append(thing_two)

    ## case where we are at leaf node
    if li_child is None:
        reqs = [Requirement(html)]
        for thing in html.next_siblings:
            reqs.append(Requirement(thing))
        ##req.print_info()
        ##print(req.get_html())
        ##req.print_info()
        ##print(getattr(req,'type'))

        return reqs

    ##Going downwards

    ##Are there more list elements nested? if so visit them
    if li_child is not None and (li_child not in visited_set):
        visited_set.add(li_child)

        child_req_array = find_sub_reqs_recursive_revised(li_child, True)

    ## end of the path that doesnt end with leaf node
    ##print('done with path:', html)
    req = Requirement(html)

    if is_head:
        sibling_req.insert(0, req)

        req.set_sub_reqs(child_req_array)
        return sibling_req

    req.set_sub_reqs(child_req_array)
    req.my_map['sub reqs' ] = None
    return req


class ReqType(Enum):
    COURSES = auto()
    UNITS = auto()
    REQUIREMENTS = auto()


def determineType(req_html):
    if req_html.text.__contains__('Complete') or req_html.text.__contains__('complete'):
        return ReqType.REQUIREMENTS
    ##if req_html.text.__contains__():
    ##   return ReqType.COURSES
    if req_html.text.__contains__('units of'):
        return ReqType.UNITS

    return ReqType.COURSES


def traverse_reqs(req):
    ##req.print_info()
    if req.sub_reqs is not None:
        for thing in req.sub_reqs:
            traverse_reqs(thing)


def get_data(source_html) -> list:
    ##Start up beautiful soup and create a dictionary for holding different fields
    soup = BeautifulSoup(source_html, 'lxml')
    infomap = {}

    ##Wait for desired elements to load then put them into a map

    info_array = soup.find_all('div', class_='noBreak')

    ##class ="course-view__label___FPV12"
    for thing in info_array:
        section_name = thing.find(class_='course-view__label___FPV12').text
        print(section_name)
        infomap[section_name] = thing



    total_pre_reqs = infomap["Prerequisites"].find('ul', recursive=True)

    req = find_sub_reqs_wrapper(total_pre_reqs)
    print(req.my_map)

    class_code_title_map = get_class_name(soup)

    infomap["Class code"] =class_code_title_map["class code"]
    infomap["Class description"] = class_code_title_map["class description"]

    num_required = []

    total_list_eles = total_pre_reqs.find('li', recursive=True).find('li', recursive=True)

    ## for thing in total_list_eles.next_siblings:
    ## print(thing,'\n')

    final_info_map = {
        "CourseName": "course name",
        "Units": "units",
        "Prereqs": "prereqs",
        "Coreqs": "coreqs",
        "Notes": "notes"

    }

    traverse_reqs(req)


def get_class_name(html) -> map:
    class_name = html.find('div', class_= 'course-view__itemTitleAndTranslationButton___36N-_').text
    end_of_class_num = None
    start_of_class_desc = None
    class_code = []
    class_desc = []
    for i in range (0, len(class_name)):
        ##Go up until we have found hypen
        current_char = class_name[i]

        if ord(current_char) == ord("-"):
            end_of_class_num = i -1
            start_of_class_desc = i+2
            break

    for x in range(0, end_of_class_num):
        #print(x)
        class_code.append(class_name[x])
        #print(class_code[x], end= ".")

    print("\n")
    for y in range(start_of_class_desc, len(class_name)):
        class_desc.append(class_name[y])

        #print(class_name[y], end= ".")
    ##class_name_and_desc = [class_name[],]
    print("\n")
    return {
        "class code" : ''.join(class_code),
        "class description" : ''.join(class_desc)
        }


local_html = open('STAT261.html', 'r')
data = get_data(local_html)
