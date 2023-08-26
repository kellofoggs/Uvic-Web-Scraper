from bs4 import BeautifulSoup
import requests

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