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

