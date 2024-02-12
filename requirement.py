from enum import Enum, auto
import re
import utilities

# Regex for strings that start with letters and end with some number with a hyphen in the middle
class_code_regex = "^[A-Za-z\\-0-9]+\\S"
class_code_regex = "^([A-Z]+)\\S*[0-9]+.*"
has_numerals_regex = "\\d"
has_letters_regex = "[A-Za-z].+"
is_number_of_units_regex = "\\(\\d\\)"

class ReqType(Enum):
    COURSES = auto()
    UNITS = auto()
    REQUIREMENTS = auto()
    OTHER = auto()






def determine_type(req_html):
    # print(req_html.text)
    if req_html.text.__contains__("Complete") or req_html.text.__contains__("complete"):
        return ReqType.REQUIREMENTS

    if req_html.text.__contains__("units of"):
        return ReqType.UNITS


    if re.search(class_code_regex, req_html.text) is not None:
        if re.search(has_numerals_regex, req_html.text) is not None:
            return ReqType.COURSES

    return ReqType.OTHER


def reqtype_to_string(input_type):
    output = None
    if input_type == ReqType.COURSES:
        return "course"
    if input_type == ReqType.REQUIREMENTS:
        return "requirement"
    if input_type == ReqType.OTHER:
        return "other"
    if input_type == ReqType.UNITS:
        return "units"

'''
# Class for requirements. A requirement could be a singular class, a certain amount of 
units or a collection of the other 2
'''


class Requirement:
    #Class variables

    #What type of requirement the requirement is, types listed in ReqType Enum
    type = None

    course_code = None
    course_description = None
    name = None
    sub_reqs = None
    quantity = ""
    html = None
    sub_maps = None
    is_complete_all = False

    alphanumeric_window = []

    # Constructor for requirement call
    def __init__(self, doc):
        self.type = determine_type(doc)
        self.name = doc.text
        self.html = doc
        self.sub_reqs = []
        self.sub_maps = []
        # print(self)

        if self.type == ReqType.REQUIREMENTS:
            self.prep_for_reqs()
        elif self.type == ReqType.COURSES:
            self.prep_for_courses()

        elif self.type == ReqType.UNITS:
            self.prep_for_units()
        elif self.type == ReqType.OTHER:
            self.prep_for_other()

    '''
    Family of functions cleans up quantity of their respective types
    '''

    # Sets the quantity for a course type requirement, a courses "quantity" is the amount of credits it is worth
    def clean_up_course_quantity(self, soup):
        output = 0
        is_number_of_units_regex = "\\([0-9\\.]+\\)$"
        source_text = soup.text
        x = re.findall(is_number_of_units_regex, source_text)
        for string in x:
            new_string = string[1:len(string) - 1]
            output = new_string
        # print(output)
        return str(output)

    # Sets the quantity for a requirement type requirement
    def clean_up_reqs(self):
        target_string = self.html.text
        suspected_quantity = "0"

        # Use KMP search algorithm to find where "Complete" is
        #location_of_complete = utilities.KMPSearch("Complete", target_string)

        #Split target string by spaces
        target_array = target_string.split(" ")

        return target_array[1]

        # If we have all as our quantity then set bool to true


        # This allows for quantity to be incremented when sub-req is added
        self.is_complete_all = True

        #Else
        self.quantity = suspected_quantity

        return


    def clean_up_other(self, soup):
        return

    def clean_up_units(self, soup):
        self.quantity = self.html.text
        return




    #Sets the sub maps to the proper value --obsolete
    def set_sub_maps(self):
        if self.sub_reqs is not None and len(self.sub_reqs) > 0:
            for requirement in self.sub_reqs:
                # print(requirement.html.text)
                self.sub_maps.append(requirement.return_info())
        #self.clean_up_quantity(self.html)

    def prep_for_other(self):
        return

    def prep_for_courses(self):
        self.name = utilities.fetch_course_code(self.html.text)

        self.quantity = self.clean_up_course_quantity(self.html)
        #self.fetch_course_title()

        #self.fetch_course_units()

    def prep_for_reqs(self):
        self.name = "Complete"


        # find the quantity from the complete "of" line
        self.quantity = self.clean_up_reqs()
        # self.quantity = self.html.text
        return

    def prep_for_units(self):
        self.clean_up_units(self.html)

    #Does most of the work for prep for reqs,

    def get_html(self):
        return self.html

    def print_info(self):
        my_info = self.return_info()

        print(my_info)
        # print(self.html.text)



    def return_info(self):
        my_info = {
            "type": reqtype_to_string(self.type),
            "name": self.name,
            ##"course_title": self.course_title,
            "quantity": self.quantity,

            ##"sub reqs": self.sub_reqs,
            ##'sub req names': [x in self.sub_reqs.name]
            "sub maps": self.sub_maps
        }
        return my_info


    def add_to_sub_reqs(self, element):
        self.sub_reqs.append(element)
        self.sub_maps.append(element.return_info())

        #self.quantity = element.quantity + self.quantity

    def set_sub_reqs(self, in_array):
        self.sub_reqs = in_array
        self.set_sub_maps()



