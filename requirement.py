from enum import Enum, auto

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
    sub_maps = None

    def __init__(self, doc):
        self.type = determineType(doc)
        self.name = doc.text
        self.html = doc
        self.sub_maps = []

        if self.type == ReqType.REQUIREMENTS:
            self.prep_for_reqs()
        elif self.type == ReqType.COURSES:
            self.prep_for_courses()

        elif self.type == ReqType.UNITS:
            self.prep_for_units

        '''      self.my_map = {
            'type': self.type,
            'name': self.name,
            'course_title': self.course_description,
            'sub reqs': self.sub_maps,
            'quantity': self.quantity
        }'''

        ##print(self)
        return

    def set_sub_maps(self):
        if self.sub_reqs is not None and len(self.sub_reqs) > 0:
            ##print("I am ", self.name, "These are my subreqs:")

            for requirement in self.sub_reqs:
                ##print(requirement.return_info())
                self.sub_maps.append(requirement.return_info())

    def prep_for_courses(self):
        hyphen_location = None
        found_title = False

        ##if self.type == ReqType.COURSES:
        course_long = []
        string_number_array = []
        link = self.html.find("a")
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
                    course_long.pop(len(course_long) - 1)

                    ##print(''.join(course_long))
                    self.course_title = "".join(course_long)

                    found_title = True
                ##If we found the '(' before the number then we can go further into the string to look for the credit amount
                continue

            ##Find the credits that the course has
            if found_title:
                if ord(char) in range(48, 57) or ord(char) == 46:
                    string_number_array.append(char)
                elif ord(char) == 41:
                    to_be_converted_to_int = "".join(string_number_array)
                    self.quantity = float(to_be_converted_to_int)
                    return

    def prep_for_reqs(self):
        self.name = "Complete"

        ## find the quantity from the complete "of" line

        self.quantity = 0
        return

    def prep_for_units(self):
        return 0

    def get_html(self):
        return self.html

    def print_info(self):
        my_info = self.return_info()

        print(my_info)
        print(self.html.text)

    '''def return_info(self):
        my_info = {
            ##'type': self.type,
            "name": self.name,
            "course_title": self.course_description,
            "sub reqs": self.sub_reqs,
            ##'sub req names': [x in self.sub_reqs.name]
            "sub maps": self.sub_maps,
            "quantity": self.quantity

        }
        return my_info
    '''

    def return_info(self):
        my_info = {
            ##'type': self.type,
            "name": self.name,
            ##"course_title": self.course_title,
            "quantity": self.quantity,

            ##"sub reqs": self.sub_reqs,
            ##'sub req names': [x in self.sub_reqs.name]
            "sub maps": self.sub_maps

        }

        return my_info

    ## def sub_reqs_to_map(self):

    def add_to_sub_reqs(self, element):
        self.sub_reqs.append(element)

    def set_sub_reqs(self, in_array):
        self.sub_reqs = in_array
        ##print(in_array)
        ##print(self.name, self.sub_reqs)
        ##self.my_map["sub reqs"]
        ##self.set_sub_maps()

        ##print(self.name,self, "  :", self.sub_maps)
        self.set_sub_maps()
        ##print("\n")

    def clean_up_quantity(self, input):
        if self.type == ReqType.REQUIREMENTS:
            self.sub_reqs = []
            quantity = int(self.html.find("span").text)

        if self.type == ReqType.COURSES:
            quantity = int(self.html.find(
                "span").text)  ##get the span element then get its text then remove the last 5 characters and remove parantheses


class ReqType(Enum):
    REQUIREMENTS = auto()
    COURSES = auto()
    UNITS = auto()


def determineType(requirement_html):
    if requirement_html.text.__contains__("Complete", "complete"):
        return ReqType.REQUIREMENTS
    if requirement_html.text.__contains__("units of"):
        return ReqType.UNITS
    return ReqType.COURSES

