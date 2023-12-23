import os

from bs4 import BeautifulSoup
from enum import Enum, auto
import unittest
import requests
import requirement
from requirement import Requirement, ReqType
import json
import re


# Test with CSC 205
# Offline test for html scraping, does not require selenium
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
num_called = 0




def find_sub_reqs_wrapper(html):
    global visited_set
    visited_set = set()  ##reset visited set
    #req = find_sub_reqs_recursive_revised(html, False)
    if html.name != "li":
        html = html.find("li")
    req = find_sub_reqs(html, True)
    #print(req)
    return req


##On first call html is a ul

##Modified dfs for prereq searching
##Returns a requirement object that holds nested maps of other requirements under neath it and so on
def find_sub_reqs_recursive_revised(html, is_head):

    child = html.find("li", recursive= True)

    sibling_li_list = []
    sibling_req = []
    child_req_array = []
    li_child = html.find("li", recursive=True)
    #print(html.text)
    #print(html.name)
    for thing in html.next_siblings:
        if thing.name == "li":
            sibling_li_list.append(thing)

    for li in sibling_li_list:
        if li not in visited_set:
            thing_two = find_sub_reqs_recursive_revised(li, False)
            sibling_req.append(thing_two)

    ##Can only find leaf node when going down
    ## case where we are at leaf node
    if li_child is None and li_child not in visited_set:
        reqs = [Requirement(html)]
        visited_set.add(html)

        for thing in html.next_siblings:
            visited_set.add(thing)
            reqs.append(Requirement(thing))

        return reqs

    ##Going downwards

    ##Are there more list elements nested? if so visit them
    if li_child is not None and (li_child not in visited_set):
        visited_set.add(li_child)

        child_req_array = find_sub_reqs_recursive_revised(li_child, True)

    ## end of the path that doesnt end with leaf node
    req = Requirement(html)

    if is_head:
        req.set_sub_reqs(child_req_array)
        sibling_req.insert(0, req)

        return sibling_req

    req.set_sub_reqs(child_req_array)
    return req


def find_sub_reqs(html, is_head, parent_req=None) -> Requirement:

    print(html.name)
    print(html.text)

    requirement = Requirement(html)

    global visited_set

    # Visit current node
    visited_set.add(html)

    # Visit siblings if any
    if is_head:
        sideways_traversal(html, parent_req)


    # Get the first list item in the html
    li_child = html.find("li", recursive=True)



    #When we're not at the head node

    ##Case where we're at the leaf node in the HTML list tree
    if (li_child is None):
        #If there are siblings run algorithm on siblings sibling no
        if parent_req is not None:
            parent_req.add_to_sub_reqs(requirement)
        return

    else :
        #Go down until we find the last level, every time we go down the node we visit is the head
        if parent_req is not None:
            parent_req.add_to_sub_reqs(requirement)
        find_sub_reqs(li_child, True, parent_req= requirement)
        return

    return requirement


def sideways_traversal(html, parent_req = None):
    siblings = html.find_next_siblings()

    if siblings is not None and len(siblings) > 0:
        #print("Same level")
        for element in siblings:
            new_element = element
            if new_element.name != "li":
                new_element = new_element.find("li")
            find_sub_reqs(new_element, False, parent_req)


def traverse_reqs(req):
    if req.sub_reqs is not None and len(req.sub_reqs) > 0:
        for thing in req.sub_reqs:
            ##Go down
            sub_req = traverse_reqs(thing)
            req.sub_maps.append(sub_req.return_info())
            ##if sub_req is not None:
            # print(sub_req.sub_maps)

            ##req.sub_maps.append(sub_req.return_info())

    #    print("\n")
    ##req.print_info()
    return req


def get_data(source_html) -> dict:
    ##Start up beautiful soup and create a dictionary for holding different fields
    soup = BeautifulSoup(source_html, "lxml")
    source_html.close()


    #print(source_html)
    infomap = {}


    ##Wait for desired elements to load then put them into a map
    info_array = soup.find_all("div", class_="noBreak")
    for thing in info_array:
        section_name = thing.find(class_="course-view__label___FPV12").text

       # print(section_name)

        infomap[section_name] = thing

    coreqs = {}
    total_pre_reqs = {}
    req = {}
    hours = []
    course_description = None
    department = None


    if "Prerequisites" in infomap.keys():
        total_pre_reqs = infomap["Prerequisites"].find("ul", recursive=True)
        req = (find_sub_reqs_wrapper(total_pre_reqs))
               #.return_info())

    if "Units" in infomap.keys():
        units = get_class_units(infomap["Units"])
    ##Get the class code and class name
    class_code_title_map = get_class_name(soup)


    if "Hours: lecture-lab-tutorial" in infomap.keys():
        hours = get_class_hours(infomap["Hours: lecture-lab-tutorial"])
    # Not every course has coreqs so initialize as none type

    if "Description" in infomap.keys():
        course_description = get_class_description(infomap["Description"])


    if "Course offered by" in infomap.keys():
        department = get_departments(infomap["Course offered by"])

    if "Pre- or corequisites" in infomap.keys():
        ## If there are coreq section then look for coreqs
        coreqs = find_sub_reqs_wrapper(infomap["Pre- or corequisites"].find("ul", recursive=True))
        #.return_info()
        ##print("There is no coreqs")

    final_info_map = {
        "CourseCode": class_code_title_map["class code"],
        "CourseName": class_code_title_map["class name"],
        "CourseDescription": course_description,
        "Units": units,
        "Hours": hours,
        #"Notes": infomap["Note(s)"].text,
        "Department":department,

        "Prereqs": req,
        # Not every course has coreqs so initialize as empty map first
        "Coreqs": coreqs

    }
    #print(infomap["Hours: lecture-lab-tutorial"].text)
##    print(infomap["Description"].find("div").text)

    return final_info_map


    ##print("num called:", num_called)
    with open("results.json", "w") as json_file:
        ##json.dump(req.return_info(), json_file, indent=2)
        json.dump(final_info_map, json_file, indent=2)
        #json.dump(final_info_map, json_file, indent=2)



def get_class_notes(source_soup) -> list:
    notes_list_head = source_soup.find("li")
    notes_lost = []
    for thing in notes_list_head.next_siblings:
        print("A")

def get_class_description (description) -> str:
    return description.find("div").text

# Returns a map with class code and description
def get_class_name(soup) -> dict:
    class_name = soup.find("div", class_="course-view__itemTitleAndTranslationButton___36N-_").text
    end_of_class_num = None
    start_of_class_name = None
    class_code = []
    class_desc = []
    for i in range(0, len(class_name)):
        ##Go up until we have found hypen
        current_char = class_name[i]

        if ord(current_char) == ord("-"):
            end_of_class_num = i - 1
            start_of_class_name = i + 2
            break

    for x in range(0, end_of_class_num):
        class_code.append(class_name[x])

    ##print("\n")
    for y in range(start_of_class_name, len(class_name)):
        class_desc.append(class_name[y])

    return {
        "class code": "".join(class_code),
        "class name": "".join(class_desc)
    }


# Takes in the hours sections and returns a map with each section's hours required
def get_class_hours(soup) -> dict:
    hours = soup.find(class_="course-view__pre___2VF54").text.split('-')
    # Text in hours has the following format: "lecture, lab, tutorial'
    hours_map = {
        "Lecture": (hours[0]),
        "Lab": (hours[1]),
        "Tutorial": (hours[2])
    }

    return hours_map


# Gets the amount of credits in the main class being queried
def get_class_units(soup):
    if soup.find(class_="style__noFade___3YZlf").text.__contains__("or"):
        return 1.5

    return (soup.find(class_="style__noFade___3YZlf").text)
def get_departments(soup) ->str():
    return soup.find("div").text


def save_all_class_info():
    
    with open ("results.json", "w") as results_file:
        list_of_class_maps = []
        os.chdir(r"./HTML")

        for filename in os.listdir("."):
            with open(filename, 'r',encoding="utf8") as html_file:
                #print(filename)
                class_dict = get_data(html_file)
                list_of_class_maps.append(class_dict)

        json.dump(list_of_class_maps, results_file, indent=2)

'''
print(ord('A'))
print(ord('Z'))
print(ord('0'))
print(ord('9'))
print(ord('-'))
local_html = open("STAT261.html", "r")
local_html = open("CSC205.html", "r")
local_html = open("./HTML/1023.html", "r")
local_html = open("./HTML/1233.html", 'r')
#local_html = open("./HTML/1728.html", encoding="utf8")
'''
local_html = open("./HTML/727.html")
local_html = open("./HTML/703.html")

data = get_data(local_html)

#save_all_class_info()
# class_code_regex = "^[A-Za-z\\-]+.*\\s{0,2}-\\s{0,2}[0-9]+$"

class_code_regex = "^[A-Za-z\\-0-9]+"
has_numerals_regex = "\d"

code = "EDCI307A - Art in the Elementary or Middle Classroom I (1.5)"
x = re.findall(class_code_regex, code)
print(x)




