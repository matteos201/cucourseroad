from bs4 import BeautifulSoup
import requests

def webscrape_courses(department):
    '''
    Gathers entire course catalog of course names with their department, course number, credit amount, and title.
    Returns dictionary courses_dict: 
        Keys: Course IDs
        Values: Course Titles
    '''
    html_text = requests.get(f'https://catalog.colorado.edu/courses-a-z/{department}/').text
    soup = BeautifulSoup(html_text, 'lxml')
    courses = soup.find_all('div', class_ = "courseblock")
    courses_dict = {}
    for course in courses:
        curr_course = course.find('p', class_ = "courseblocktitle noindent").text
        course_num = curr_course[5:9]
        courses_dict[course_num] = curr_course
    return courses_dict

def semester_and_year():
    sem_choices = {'1': 'Fall', '2': 'Spring', '3': 'Summer'}
    year_choices = {'1': '2024', '2': '2025', '3': '2026', '4': '2027', '5': '2028', '6': '2029'}
    valid_input1, valid_input2 = False, False
    while not valid_input1 or not valid_input2:
        semester = input("Pick your semester\n------------\n1. Fall\n2. Spring\n3. Summer\n")
        if semester in sem_choices:
            valid_input1 = True
        else:
            print("Failed to identify semester choice: Please enter 1, 2, or 3.")
        year = input("Pick your year\n-------------\n1. 2024\n2. 2025\n3. 2026\n4. 2027\n5. 2028\n6. 2029\n")
        if year in year_choices:
            valid_input2 = True
        else:
            print("Failed to identify year choice: Please enter 1, 2, or 3, 4, 5, or 6.")
    return (semester, year)

def course_selection(courses_catalog):
    my_courses = []
    end = False
    while not end:
        user_input = input("Please insert course number (enter 'quit' to quit prompt): ")
        if user_input == 'quit':
            end = True
        elif user_input in courses_catalog:
            my_courses.append(courses_catalog[user_input])
        else:
            print("Cannot identify course number")
    return my_courses



if __name__ == "__main__":
    sem_and_year = semester_and_year()
    course_catalog = webscrape_courses(input("Please choose your department: "))
    my_courses = course_selection(course_catalog)

    

    print(my_courses)