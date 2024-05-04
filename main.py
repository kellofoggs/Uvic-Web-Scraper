import os
import bs4
from bs4 import BeautifulSoup
import selenium_scraper
from requirement import Requirement, ReqType
import utilities
import json
import re
import selenium.webdriver as webdriver

proper_title_pattern = "\\s-\\s"
# Set for DFS that is reinitialized whenever wrapper is called
visited_set = None
num_called = 0
req_course_list = []

'''
Wrapper for recursive function "find_sub_reqs"
@:return
 returns a "requirement" object which is a multi-level dictionary of pre/co requisites
@:parameter
 html: a beautiful soup object used to parse HTML which the object has been given
'''


def find_sub_reqs_wrapper(html: bs4.BeautifulSoup):
    global visited_set
    visited_set = set()  ##reset visited set

    global req_course_list  ## Reset req_course_list
    req_course_list = []

    # # Find the first list in pre reqs section, we don't have to worry about edge case in recursive function here
    # if html.name != "ul":
    #     html = html.find("ul")

    html = bfs_find(html, ["li"])

    req = find_sub_reqs_revision(html, True)
    # req.print_info()
    return req


'''
Recursive function for finding all the sub reqs of a requirement and adding them to "requirement" object fields
@:parameter
 html: a beautiful soup object that represents the HTML of the item currently being looked at
 is_branch_head: a boolean that tells whether or not the current item is the first in its level
 parent_req: A reference to another "requirement" object that the current requirement is a sub-requirement to
@:return
 The head requirement object which must be fulfilled dby fulfilling its sub reqs.
'''
# Encountered edge case, seems that beautiful soup uses dfs by default to search for tags
# Therefore it may find a case like :
'''
<ul>
    <div>
        <span>

        </span>
        <li>
            <span>Complete <!-- -->1<!-- --> of the following</span>
            <ul>
                <li data-test="ruleView-A.1">
                    <div data-test="ruleView-A.1-result">
                        <div>Foundations of Math 12</div>
                    </div>
                </li>
                <li data-test="ruleView-A.2"><div data-test="ruleView-A.2-result">
                    <div>
                        Mathematics 12</div>
                    </div>
                </li>
                <li data-test="ruleView-A.3">
                    <div 
                        data-test="ruleView-A.3-result">
                        <div>Pre-Calculus 12</div>
                    </div>
                </li>
            </ul>
        </li>
    </div>
    <li data-test="ruleView-D">
        <div data-test="ruleView-D-result">Complete <span>1</span> of: <div>
            <ul style="margin-top:5px;margin-bottom:5px">
                <li><span><a href="#/courses/view/63168b42bee727d381e640aa">MATH100</a> <!-- -->-<!-- --> <!-- -->Calculus I<!-- --> <span style="margin-left:5px">(1.5)</span></span></li>
                <li><span><a href="#/courses/view/63168c6ccdd330aecb502b3d">MATH102</a> <!-- -->-<!-- --> <!-- -->Calculus for Students in the Social and Biological Sciences<!-- --> <span style="margin-left:5px">(1.5)</span></span></li>
                <li><span><a href="#/courses/view/63168d043e376f0b1f621ffd">MATH109</a> <!-- -->-<!-- --> <!-- -->Introduction to Calculus<!-- --> <span style="margin-left:5px">(1.5)</span></span></li>
                <li><span><a href="#/courses/view/63168d5cbee7272a8be640b9">MATH120</a> <!-- -->-<!-- --> <!-- -->Precalculus Mathematics<!-- --> <span style="margin-left:5px">(1.5)</span></span></li>
            </ul>
        </div>
    </div>
    </li>
</ul>
'''
#
#
# # Where the div path is followed, and the li in the same level is ignored.
# def find_sub_reqs(html, is_branch_head, parent_req=None):
#     # Generate a 'Requirement' object from the current HTML element that is a list item
#     global req_course_list
#     # print(html)
#     current_req = Requirement(html, req_course_list)
#
#     # print(html.find_all(recursive=False))
#
#     resolve_tree(html, 0)
#     # Bring in the visited set from global scope
#     global visited_set
#
#     # Visit current node
#     visited_set.add(html)
#
#     # Visit siblings if any
#     if is_branch_head:
#         sideways_traversal(html, parent_req)
#
#     # Get the first list item in the html
#     li_child = html.find("li", recursive=True)
#
#     # When we're not at the root node
#     if parent_req is not None:
#
#         # Case where we're at the leaf node in the HTML list tree (this generally results in a "course" req or "other"
#         # type of req
#         if li_child is None:
#             parent_req.add_to_sub_reqs(current_req)
#
#             # If there are siblings run algorithm on siblings sibling no
#             return
#
#         else:
#
#             # Go down until we find the last level, every time we go down the node we visit is the head
#
#             find_sub_reqs(li_child, True, parent_req=current_req)
#             parent_req.add_to_sub_reqs(current_req)
#
#             return
#     else:
#         if li_child is not None:
#             find_sub_reqs(li_child, True, parent_req=current_req)
#     return current_req


# Assume that html is a ul or li item to start
def find_sub_reqs_revision(html: bs4.BeautifulSoup, is_branch_head: bool, parent_req: Requirement = None):
    # Generate a 'Requirement' object from the current HTML element that is a list item
    global req_course_list
    # print(html)
    current_req = Requirement(html, req_course_list)

    # print(html.find_all(recursive=False))

    # resolve_tree(html, 0)
    # Bring in the visited set from global scope
    global visited_set

    # Visit current node
    visited_set.add(html)

    # Visit siblings if any
    if is_branch_head:
        sideways_traversal(html, parent_req)

    # Get the first list item in the html
    li_child = bfs_find(html, target_tags = ["li"])

    # When we're not at the root node
    if parent_req is not None:

        # Case where we're at the leaf node in the HTML list tree (this generally results in a "course" req or "other"
        # type of req
        if li_child is None:
            parent_req.add_to_sub_reqs(current_req)

            # If there are siblings run algorithm on siblings sibling no
            return

        else:

            # Go down until we find the last level, every time we go down the node we visit is the head

            find_sub_reqs_revision(li_child, True, parent_req=current_req)
            parent_req.add_to_sub_reqs(current_req)

            return
    # Parent req is only none when we're at the root node
    else:
        if li_child is not None:
            find_sub_reqs_revision(li_child, True, parent_req=current_req)
    return current_req

    pass


# searches by tag name/ html id to avoid same level error
def bfs_find(html: bs4.BeautifulSoup, target_tags: [] = ["li", "ul"]):
    to_visit = []
    to_visit.append(html)
    current_level_items = 0
    global visited_set

    # visited = set()
    # It may be the case that the li or ul is not the first elenent in the tree structure
    # In such a case we want to get both next and prev siblings for sideways traver    while len(to_visit) > 0:
    current = to_visit.pop(0)
    to_visit.extend(current.find_all(recursive=False))
    while len(to_visit) > 0:
        current = to_visit.pop(0)

        # When we have found the first li, or ul return it
        if current.name in target_tags:
            # print(current)
            return current
        # elif current.name == "li":
        #     pass

        visited_set.add(current)
        potential_next = (current.find_all(recursive=False))

        for item in potential_next:
            if item not in visited_set:
                to_visit.append(item)


    pass


# First check if there are any list elements or unordered lists in the current layer, at the first sight of one return list of elements
def resolve_tree(html, level):
    # print(html)
    possible_subs = html.find_all(recursive=False)
    list_under = False
    list_is = []

    # Check in same level first
    for i in range(0, len(possible_subs)):
        sub = possible_subs[i]
        # print(sub)

        # Is the current list element a list? if so return that element along with the level it was found at
        if sub.name in ["ul", "li"]:
            list_under = True
            # list_is.append(i)
            # print("There's a list somewhere")

            return level, sub
            # Stop at the first list in level
            break

        # If there is no list element anywhere down the tree then drop the element.
        if sub.find("li") is None:
            # print("No sub lists")
            continue
        else:
            list_is.append(i)

        optimal_lis = []
    for ele in list_is:
        optimal_lis.append(ele)
        # print(f"HH {ele}")
    # return resolve_tree()

    # print("\n\n")

    pass


''' Looks at sibling requirements in the same 'level' as current requirements
    @:argument
    html: BeautifulSoup object that represents the 'head' of a level
    parent_req: The parent of the prerequisites in the same level. Each level has 1 parent at most
'''


def sideways_traversal(html, parent_req=None):
    siblings = html.find_next_siblings()
    if siblings is not None:
        siblings.extend(html.find_previous_siblings())
    else:
        siblings = html.find_previous_siblings()

    if siblings is not None and len(siblings) > 0:
        for element in siblings:
            new_element = element
            if new_element.name != "li" and new_element.name != "ul":
                # print(f"sideways {new_element}")
                new_element = new_element.find("li")
                if new_element is None:
                    continue
            # if new_element == None:
            #     new_element = new_element.find("ul")
            find_sub_reqs_revision(new_element, False, parent_req)


'''
Prepares a map for writing to a JSON file 
'''


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
    units = None

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
        notes = infomap["Note(s)"].find("div").text
    if "Prerequisites" in infomap.keys():
        total_pre_reqs = infomap["Prerequisites"].find("ul", recursive=True)
        req = (find_sub_reqs_wrapper(total_pre_reqs).return_info())
        # print(req)

    # Map of information of a class
    final_info_map = {

        "courseCode": class_code_title_map["class code"],
        "courseName": class_code_title_map["class name"],
        "courseDescription": course_description,
        "units": units,
        "hours": hours,
        "notes": notes,
        "department": department,

        "prereqs": req,
        # Not every course has coreqs so initialize as empty map first
        "coreqs": coreqs  # ,
        # "prereqCourses": req_course_list

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
    # for thing in notes_list_head.next_siblings:


def get_class_description(description) -> str:
    return description.find("div").text


def get_class_code(soup):
    class_name_region = soup.find("div", class_="course-view__itemTitleAndTranslationButton___36N-_").text
    return utilities.fetch_course_code(class_name_region)


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
        # We want to throw an error here and have handling function handle it
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

    "".join()


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


# Saves all class info from pregened html files
def save_all_class_info():
    with open("results.json", "w", encoding="ASCII") as results_file:
        list_of_class_maps = []
        os.chdir("./HTML")
        count = 0
        for filename in os.listdir("."):
            # print(filename)
            with open(filename, 'r', encoding="utf8") as html_file:
                # print(filename)
                class_dict = get_data(html_file)
                list_of_class_maps.append(class_dict)
        # print(count)
        os.chdir("..")
        json.dump(list_of_class_maps, results_file, indent=2)


# save all class info from html gotten by selenium without saving on disk
def save_class_info_inplace():
    with open("results.json", "w", encoding="ASCII") as results_file:
        list_of_class_maps = []
        # browser_options = webdriver.EdgeOptions()
        # browser_options.headless= False
        # driver = webdriver.Edge()
        for link in selenium_scraper.get_all_class_links():
            html_source = selenium_scraper.render_html(link)
            class_dict = get_data(html_source)
            list_of_class_maps.append(class_dict)
        json.dump(list_of_class_maps, results_file, indent=2)


# fi = open('HTML/Current=CSC110%20-%20Fundamentals%20of%20Programming%20I&bcGroup=Computer%20Science%20')
# class_dict = get_data(fi)
# with open("new_res", "w") as results_file:
#     json.dump(class_dict, results_file, indent=2)

# print(class_dict)
save_all_class_info()
# save_class_info_inplace()
# re.search("\d+\\.*\d*
# units of", "4.5 units of 300- or 400-level GNDR or WS courses")
