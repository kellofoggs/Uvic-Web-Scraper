import os

from bs4 import BeautifulSoup
from enum import Enum, auto
import unittest
import requests
import requirement
from requirement import Requirement, ReqType
import utilities
import json
import re
proper_title_pattern = "\\s-\\s"
# Set for DFS that is reinitialized whenever wrapper is called
visited_set = None
num_called = 0


def find_sub_reqs_wrapper(html):
    global visited_set
    visited_set = set()  ##reset visited set
    # req = find_sub_reqs_recursive_revised(html, False)
    if html.name != "li":
        html = html.find("li")
    req = find_sub_reqs(html, True)
    return req




# Modified dfs for pre req searching
# Returns requirement object that knows its sub requirements

'''def find_sub_reqs(html, is_head, parent_req=None) -> Requirement:
    #print(html.name)
    #print(html.text)
    1
    requirement = Requirement(html)

    global visited_set

    # Visit current node
    visited_set.add(html)

    # Visit siblings if any
    if is_head:
        sideways_traversal(html, parent_req)

    # Get the first list item in the html
    li_child = html.find("li", recursive=True)

    # When we're not at the head node
    if parent_req is not None:
        # Case where we're at the leaf node in the HTML list tree
        if li_child is None:
            # If there are siblings run algorithm on siblings sibling no
            parent_req.add_to_sub_reqs(requirement)
            if html.siblings is None or len(html.siblings) <= 0:
                parent_req.set_sub_maps()
            return

        else:

            # Go down until we find the last level, every time we go down the node we visit is the head
            parent_req.add_to_sub_reqs(requirement)
            if html.siblings is None or len(html.siblings) <= 0:
                parent_req.set_sub_maps()
            find_sub_reqs(li_child, True, parent_req=requirement)
            return
    else:
        if li_child is not None:

            find_sub_reqs(li_child, True, parent_req=requirement)
        return requirement
'''


# For new find sub reqs go all the way down first then start making objects
def find_sub_reqs(html, is_head,parent_req = None):
    requirement = Requirement(html)


    global visited_set

    # Visit current node
    visited_set.add(html)

    # Visit siblings if any
    if is_head:
        sideways_traversal(html, parent_req)

    # Get the first list item in the html
    li_child = html.find("li", recursive=True)

    # When we're not at the head node
    if parent_req is not None:
        # Case where we're at the leaf node in the HTML list tree
        if li_child is None:
            # If there are siblings run algorithm on siblings sibling no
            parent_req.add_to_sub_reqs(requirement)
            return

        else:

            # Go down until we find the last level, every time we go down the node we visit is the head
            parent_req.add_to_sub_reqs(requirement)
            if html.siblings is None or len(html.siblings) <= 0:
                parent_req.add_to_sub_reqs(requirement)
            find_sub_reqs(li_child, True, parent_req=requirement)
            return
    else:
        if li_child is not None:
            find_sub_reqs(li_child, True, parent_req=requirement)
    return requirement

def sideways_traversal(html, parent_req=None):
    siblings = html.find_next_siblings()

    if siblings is not None and len(siblings) > 0:
        # print("Same level")
        for element in siblings:
            new_element = element
            if new_element.name != "li":
                new_element = new_element.find("li")
            find_sub_reqs(new_element, False, parent_req)





def get_data(source_html) -> dict:
    # Start up beautiful soup and create a dictionary for holding different fields on the site
    soup = BeautifulSoup(source_html, "lxml")

    infomap = {}

    # Wait for desired elements to load then put them into a map
    info_array = soup.find_all("div", class_="noBreak")
    for thing in info_array:
        section_name = thing.find(class_="course-view__label___FPV12").text
        infomap[section_name] = thing

    coreqs = {}
    total_pre_reqs = {}
    req = {}
    hours = []
    notes = None
    course_description = None
    department = None

    if "Prerequisites" in infomap.keys():
        total_pre_reqs = infomap["Prerequisites"].find("ul", recursive=True)
        req = (find_sub_reqs_wrapper(total_pre_reqs).return_info())
        #print(req)
    if "Units" in infomap.keys():
        units = get_class_units(infomap["Units"])
    # Get the class code and class name
    class_code_title_map = get_class_name(soup.find("title"))

    if "Hours: lecture-lab-tutorial" in infomap.keys():
        hours = get_class_hours(infomap["Hours: lecture-lab-tutorial"])
    # Not every course has coreqs so initialize as none type

    if "Description" in infomap.keys():
        course_description = get_class_description(infomap["Description"])

    if "Course offered by" in infomap.keys():
        department = get_departments(infomap["Course offered by"])

    if "Pre- or corequisites" in infomap.keys():
        # If there are coreq section then look for coreqs
        coreqs = find_sub_reqs_wrapper(infomap["Pre- or corequisites"].find("ul", recursive=True)).return_info()
    if "Note(s)" in infomap.keys():
        notes = infomap["Note(s)"].text

    final_info_map = {

        "CourseCode": class_code_title_map["class code"],
            #get_class_code(soup.find("title")),
        "CourseName": class_code_title_map["class name"],
        "CourseDescription": course_description,
        "Units": units,
        "Hours": hours,
        "Notes": notes,
        "Department": department,

        "Prereqs": req,
        # Not every course has coreqs so initialize as empty map first
        "Coreqs": coreqs

    }
    # print(infomap["Hours: lecture-lab-tutorial"].text)
    ##    print(infomap["Description"].find("div").text)

    return final_info_map

    ##print("num called:", num_called)
    with open("results.json", "w") as json_file:
        ##json.dump(req.return_info(), json_file, indent=2)
        json.dump(final_info_map, json_file, indent=2)
        # json.dump(final_info_map, json_file, indent=2)
    return final_info_map


def get_class_notes(source_soup) -> list:
    notes_list_head = source_soup.find("li")
    notes_lost = []
    for thing in notes_list_head.next_siblings:
        print("A")


def get_class_description(description) -> str:
    return description.find("div").text

def get_class_code(soup):
    class_name_region = soup.find("div", class_="course-view__itemTitleAndTranslationButton___36N-_").text
    return utilities.fetch_course_code(class_name_region)

#def check_titles_are_all_valid():

# Returns a map with class code and description
def get_class_name(class_name_region) -> dict:


    if class_name_region is not None:
        source_text = class_name_region.text
        split = re.split(proper_title_pattern, source_text)
        return {
            "class code": split[0],
            "class name": split[1]
        }

    else:
        1
        #We want to throw an error here and have handling function handle it
    '''if class_name_region is None:
        return
        #class_name_region = soup.find(ass="course-view__itemTitleAndTranslationButton___36N-_"><div><h2>ECE457 - Parallel and Cluster Computing</h2></div><div class="course-view__translationButtonContainer___1Srg0")
    class_name = class_name_region.text
    end_of_class_num = None
    start_of_class_name = None
    class_code = []
    class_desc = []
    for i in range(0, len(class_name)):
        # Go up until we have found hypen
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
    }'''


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


def get_departments(soup) -> str():
    return soup.find("div").text


def save_all_class_info():
    with open("results.json", "w") as results_file:
        list_of_class_maps = []
        os.chdir("./HTML")
        count = 0
        for filename in os.listdir("."):
            # print(filename)
            with open(filename, 'r', encoding="utf8") as html_file:
                '''soup = BeautifulSoup(html_file, "lxml")
                html_file.close()
                source = soup.find("title")
                if source is None:
                    1
                source_text = source.text
                match_found = re.search(proper_title_pattern, source_text)
                if match_found is not None:
                    count = count+1'''
                #print(filename)
                class_dict = get_data(html_file)
                list_of_class_maps.append(class_dict)
        #print(count)
        os.chdir("..")
        json.dump(list_of_class_maps, results_file, indent=2)


local_html = open("./HTML/727.html")
local_html = open("./HTML/703.html")
local_html = open("./HTML/1006.html")
local_html = open("./HTML/999.html")
local_html = open("./HTML/1284.html")
local_html  = open("./HTML/1041.html")
# get_data((local_html))
save_all_class_info()

is_number_of_units_regex = "\\(\\d\\.\\d\\)"
is_number_of_units_regex = "\\([0-9\\.]+\\)"
test_string = "MATH151 - Finite Mathematics (1.5)"
x = re.findall(is_number_of_units_regex, test_string)
#print(x)





#data = get_data(local_html)

#save_all_class_info()
# class_code_regex = "^[A-Za-z\\-]+.*\\s{0,2}-\\s{0,2}[0-9]+$"

class_code_regex = "^[A-Za-z\\-0-9]+"
has_numerals_regex = "\\d"

code = "EDCI307A - Art in the Elementary or Middle Classroom I (1.5)"
x = re.findall(class_code_regex, code)
#print(x)
