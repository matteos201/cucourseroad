from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://catalog.colorado.edu/courses-a-z/csci/').text
soup = BeautifulSoup(html_text, 'lxml')
courses = soup.find_all('div', class_ = "courseblock")
courses_dict = {}
for course in courses:
    curr_course = course.find('p', class_ = "courseblocktitle noindent").text
    course_num = curr_course[5:9]
    courses_dict[course_num] = curr_course

print(courses_dict['1300'])
my_courses = {'Summer 2024': []}
end = False
while not end:
    user_input = input("Please insert course number (enter 'quit' to quit prompt): ")
    if user_input == 'quit':
        end = True
    elif user_input in courses_dict:
        my_courses['Summer 2024'].append(courses_dict[user_input])
    else:
        print("Cannot identify course number")

print(my_courses)