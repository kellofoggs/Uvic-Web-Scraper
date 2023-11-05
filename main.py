from bs4 import BeautifulSoup
from enum import Enum, auto
import unittest
import requests
import requirement
from requirement import Requirement,ReqType
import json

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
num_called = 0




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

    li_child = html.find("li", recursive=True)
    for thing in html.next_siblings:
        if thing.name == "li":
            sibling_li_list.append(thing)

    for li in sibling_li_list:
        if li not in visited_set:
            thing_two = find_sub_reqs_recursive_revised(li, False)
            sibling_req.append(thing_two)

    ##Can only find leaf node when going down
    ## case where we are at leaf node
    if li_child is None:
        reqs = [Requirement(html)]
        for thing in html.next_siblings:
            reqs.append(Requirement(thing))

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
        req.set_sub_reqs(child_req_array)

        sibling_req.insert(0, req)

        return sibling_req

    req.set_sub_reqs(child_req_array)
    ##req.my_map['sub reqs' ] = None
    return req


class ReqType(Enum):
    COURSES = auto()
    UNITS = auto()
    REQUIREMENTS = auto()


def determineType(req_html):
    if req_html.text.__contains__("Complete") or req_html.text.__contains__("complete"):
        return ReqType.REQUIREMENTS
    ##if req_html.text.__contains__():
    ##   return ReqType.COURSES
    if req_html.text.__contains__("units of"):
        return ReqType.UNITS

    return ReqType.COURSES


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


def get_data(source_html) -> list:
    ##Start up beautiful soup and create a dictionary for holding different fields
    soup = BeautifulSoup(source_html, "lxml")
    infomap = {}

    ##Wait for desired elements to load then put them into a map
    info_array = soup.find_all("div", class_="noBreak")
    for thing in info_array:
        section_name = thing.find(class_="course-view__label___FPV12").text

        print(section_name)

        infomap[section_name] = thing

    total_pre_reqs = infomap["Prerequisites"].find("ul", recursive=True)
    req = find_sub_reqs_wrapper(total_pre_reqs)

    ##Get the class code and class name
    class_code_title_map = get_class_name(soup)
    hours = get_class_hours(infomap["Hours: lecture-lab-tutorial"])
    # Not every course has coreqs so initialize as none type
    coreqs = None

    final_info_map = {
        "CourseName": class_code_title_map["class code"],
        "CourseDescription": class_code_title_map["class description"],
        "Units": "units",
        "Hours": hours,

        "Prereqs": req.return_info(),
        # Not every course has coreqs so initialize as
        "Coreqs": "coreqs",
        "Notes": infomap["Note(s)"].text

    }
    print(infomap["Hours: lecture-lab-tutorial"].text)

    ##print("num called:", num_called)
    with open("results.json", "w") as json_file:
        ##json.dump(req.return_info(), json_file, indent=2)
        json.dump(final_info_map, json_file, indent=2)


##traverse_reqs(req)
## print(req.name,' ',req.return_info())

def get_class_notes(source_soup) -> list:
    notes_list_head = source_soup.find("li")
    notes_lost = []
    for thing in notes_list_head.next_siblings:
        print("A")


def get_class_name(soup) -> dict:
    class_name = soup.find("div", class_="course-view__itemTitleAndTranslationButton___36N-_").text
    end_of_class_num = None
    start_of_class_desc = None
    class_code = []
    class_desc = []
    for i in range(0, len(class_name)):
        ##Go up until we have found hypen
        current_char = class_name[i]

        if ord(current_char) == ord("-"):
            end_of_class_num = i - 1
            start_of_class_desc = i + 2
            break

    for x in range(0, end_of_class_num):
        # print(x)
        class_code.append(class_name[x])
        # print(class_code[x], end= ".")

    ##print("\n")
    for y in range(start_of_class_desc, len(class_name)):
        class_desc.append(class_name[y])

        # print(class_name[y], end= ".")
    ##class_name_and_desc = [class_name[],]
    ##print("\n")
    return {
        "class code": "".join(class_code),
        "class description": "".join(class_desc)
    }


# Takes in the hours sections and returns a map with each section's hours required
def get_class_hours(soup) -> dict:
    # '<div class="course-view__pre___2VF54"><div>3-1-0</div></div>'
    hours = soup.find(class_="course-view__pre___2VF54").text.split('-')
    # Text in hours has following format: "lecture, lab, tutorial'
    hours_map = {
        "Lecture": int(hours[0]),
        "Lab":int( hours[1]),
        "Tutorial": int(hours[2])
    }

    return hours_map


local_html = open("STAT261.html", "r")
data = get_data(local_html)
'''
me = {"Map":
          {"Sub map":
                  {"sub sub map": "item"}
              }
      }

print(me)
'''
