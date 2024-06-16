from bs4 import BeautifulSoup
import requests

def webscrape_depts():
    html_text = requests.get('https://catalog.colorado.edu/courses-a-z/').text
    soup = BeautifulSoup(html_text, 'lxml')
    depts_set = set()
    for dept in soup.find_all('div', id = 'atozindex')[0]:
        for li in dept.find_next('ul').find_all('li'):
            curr_dept = li.find_next('a').text
            if '(' in curr_dept:
                depts_set.add(curr_dept[curr_dept.index('(')+1:curr_dept.index(')')].lower())
    return depts_set

def webscrape_courses(department):
    '''
    Gathers entire course catalog of course names with their department, course number, credit amount, and title.
    Returns dictionary courses_dict: 
        Keys: Course IDs
        Values: Course Titles
    '''
    # Stores html text of department catalog website
    html_text = requests.get(f'https://catalog.colorado.edu/courses-a-z/{department}/').text 
    soup = BeautifulSoup(html_text, 'lxml')
    courses = soup.find_all('div', class_ = "courseblock")
    courses_dict = {}

    # Grabs titles of each course block from department website
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
        semester = input("Pick your semester\n------------\n1. Fall\n2. Spring\n3. Summer\n> ")
        if semester in sem_choices:
            valid_input1 = True
        elif semester == "quit":
            exit()
        else:
            print("Failed to identify semester choice: Please enter 1, 2, or 3.")
        year = input("Pick your year\n-------------\n1. 2024\n2. 2025\n3. 2026\n4. 2027\n5. 2028\n6. 2029\n> ")
        if year in year_choices:
            valid_input2 = True
        elif year == "quit":
            exit()
        else:
            print("Failed to identify year choice: Please enter 1, 2, or 3, 4, 5, or 6.")
    return (sem_choices[semester], year_choices[year])

def course_selection(courses_catalog):
    my_courses = []
    while True:
        user_input = input("Please insert course number (enter 'done' to finish adding courses):\n> ")
        if user_input == 'done':
            break
        elif user_input in courses_catalog:
            while True:
                confirm = input("Confirm to add this course? (y/n):\n> ").lower()
                if confirm == 'y':
                    print(f"Added {courses_catalog[user_input]}")
                    my_courses.append(courses_catalog[user_input])
                    break
                elif confirm == 'n':
                    break
                else:
                    print("Please enter n for no or y for yes")

        else:
            print("Cannot identify course number")
    return my_courses

def main():
    while True:
        
        choices = input("\nWhat would you like to do?\n> ")
        match choices:
            case "plan":
                sem_and_year = semester_and_year()
                print(f'Your semester and year: {sem_and_year}')
                break
            case "quit":
                exit()
            case _:
                print("Sorry. Your input does not match our choices.")
                continue
    avail_depts = webscrape_depts()
    while True:
        confirm = ''
        check_department = input("Please choose your department:\n> ")
        if check_department == "quit":
            exit()
        elif check_department in avail_depts:
            while True:
                confirm = input("Are you sure you want this department? (y/n) \n> ").lower()
                if confirm == 'y':
                    course_catalog = webscrape_courses(check_department)
                    my_courses = course_selection(course_catalog)
                    break
                elif confirm == 'n':
                    break
                else:
                    print("Please enter y for yes or n for no.")
        else:
            print("This is not a valid department code!")
        if confirm == 'y':
            break

    print(f"Courses picked for {sem_and_year[0]}, {sem_and_year[1]}:")
    for course in my_courses:
        print(course)
    files = []
    while True:
        save_to_file = input("Save to file? (y/n)\n> ").lower()
        match save_to_file:
            case 'y':
                file_name = f"{sem_and_year[0]}{sem_and_year[1]}.txt"
                f = open(file_name, "w")
                files.append(file_name)
                f.write(f"Courses picked for {sem_and_year[0]}, {sem_and_year[1]}:")
                for course in my_courses:
                    f.write(f"\n{course}")
                f.close()
                break
            case 'n':
                break
            case 'quit':
                exit()
            case _:
                print("Please enter y for yes or n for no.")
                continue

    main()

if __name__ == "__main__":
    print("\n\nWELCOME TO COURSEROAD FOR CU!\n----------------------------\n")
    print("--------Controls Guide--------")
    print("'quit': Quits program")
    print("'plan': Start planning semester")
    main()