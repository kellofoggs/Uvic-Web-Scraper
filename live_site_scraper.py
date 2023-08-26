from bs4 import BeautifulSoup
from helium import *
import requests


from requests_html import HTMLSession
session = HTMLSession()
course_url = 'https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses'
browser = start_chrome(course_url, headless=False)

html = browser.page_source

print(html)

'''
response = session.get(course_url)


myhtml = response.html
response.html.render(timeout= 20, sleep =10, keep_page= True, scrolldown = 3)

prereqs = response.html.find('div')
print(response.html.html)

##print(myhtml)
#for course in prereqs:
 #   print(course.text)
'''
'''
html_text = requests.get('https://www.uvic.ca/calendar/undergrad/index.php#/courses/Syd5kOaQV?bc=true&bcCurrent=CSC205%20-%202D%20Computer%20Graphics%20and%20Image%20Processing&bcGroup=Computer%20Science%20(CSC)&bcItemType=courses').text
##print(html_text)
##soup = BeautifulSoup(html_text, 'lxml')


'''

def read_individual_course(course):

    soup = BeautifulSoup(course, 'lxml')
    prereq = soup.find_all('span')
    print(prereq)

'''

    prereqs = soup.find_all('div', class_ = 'noBreak' )
    for thing in prereqs:
        print(thing, "\n")





read_individual_course(html_text)

'''
