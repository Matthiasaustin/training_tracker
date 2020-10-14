""" Provides utilities to clean up the chapter records read in via CSV from Moodle courses """
from datetime import datetime, timedelta


def hour_checker(student):
    student = student

    dd_1= 0
    dd_2= 0
    dd_3= 0
    dd_4= 0
    dd_5= 0


    for k, v in student.items():

        if k == 'Complete chapter_01':
            if student['Complete chapter_01'] == 'Finished':
                dd_1 = dd_1 + 2.5

        if k == 'Complete chapter_02':
            if student['Complete chapter_02'] == 'Finished':
                dd_1 = dd_1 + 2

        if k == 'Complete chapter_03':
            if student['Complete chapter_03'] == 'Finished':
                dd_1 = dd_1 + 2.5

        if k == 'Complete chapter_04':
            if student['Complete chapter_04'] == 'Finished':
                dd_2 = dd_2 + 4

        if k == 'Complete chapter_05':
            if student['Complete chapter_05'] == 'Finished':
                dd_3 = dd_3 + 4

        if k == 'Complete chapter_06':
            if student['Complete chapter_06'] == 'Finished':
                dd_3 = dd_3 + 1.5

        if k == 'Complete chapter_07':
            if student['Complete chapter_07'] == 'Finished':
                dd_3 = dd_3 + 2

        if k == 'Complete chapter_08':
            if student['Complete chapter_08'] == 'Finished':
                dd_4 = dd_4 + 4

        if k == 'Complete chapter_09':
            if student['Complete chapter_09'] == 'Finished':
                dd_5 = dd_5 + 4

        if k == 'Complete chapter_10':
            if student['Complete chapter_10'] == 'Finished':
                dd_5 = dd_5 + 2.5

        if k == 'Complete chapter_11':
            if student['Complete chapter_11'] == 'Finished':
                dd_4 = dd_4 + 2.5

        if k == 'Complete chapter_12':
            if student['Complete chapter_12'] == 'Finished':
                dd_5 = dd_5 + 6

        if k == 'Complete chapter_13':
            if student['Complete chapter_13'] == 'Finished':
                dd_2 = dd_2 + 1.5

        if k == 'Complete chapter_14':
            if student['Complete chapter_14'] == 'Finished':
                dd_2 = dd_2 + 2

    hours_available= 0
    hours_completed =  dd_1 + dd_2 + dd_3 + dd_4 + dd_5
    date = datetime.date(datetime.now())
    print("Course Start Date: YYYY-MM-DD")
    # start_date = datetime.strptime(input(),'%Y-%m-%d')
    start_date= datetime.strptime('2020-9-25', '%Y-%m-%d')
    start_date = datetime.date(start_date)
    if date > start_date:
        hours_available = hours_available + 13.5
    if date > start_date + timedelta(days=7):
        hours_available = hours_available + 14.5
    if date > start_date + timedelta(days=14):
        hours_available = hours_available + 14.5

    hours_outstanding = hours_available - hours_completed

    student['Due Date #1'] = dd_1
    student['Due Date #2'] = dd_2
    student['Due Date #3'] = dd_3
    student['Due Date #4'] = dd_4
    student['Due Date #5'] = dd_5
    student['Total Hours Completed'] = hours_completed
    student['Total Hours Outstanding'] = hours_outstanding 

    return student
def percent_complete(student):

    """Takes a dictionary record of chapter completion for a student and returns total number of activities, total completed and percentage"""

    # default number of activities to take away when determining total for percent
    less = 9

    # Per chapter number to take away when determining percentage
    new_less = {
        'chapter_01':10,
        'chapter_02':9,
        'chapter_03':9,
        'chapter_04':9,
        'chapter_05':9,
        'chapter_06':9,
        'chapter_07':9,
        'chapter_08':9,
        'chapter_09':9,
        'chapter_10':9,
        'chapter_11':9,
        'chapter_12':9,
        'chapter_13':9,
        'chapter_14':9
                }

    # read chapter to determine how much to take away
    less = new_less[student['Chapter']]

    # total number of activities complete = total (-) irrelevant activities.
    num_act = len(student.keys() ) - less
    num_comp = 0

    # count the number of completed activities in student's record
    for k,v in student.items():
        if 'Completed' in str(v):
            num_comp = num_comp + 1

    # produces percentage as int
    percent = int(100*( num_comp/num_act))

    # returns the number of activities complete,
    # how many there are total and the percentage
    return([num_comp,num_act,percent])


def clean_data(chapter_list):
    """A function that processes a list of student records for a chapter and produces a cleaner output to use in other functions"""
    clean_chapter = []
    # create a list of chapter activities based on the first entry
    chapter_activities = list(chapter_list[0].keys())

    # loop the list and remove completion dates
    for i in chapter_activities:
        if "Completion date" in str(i):
            chapter_activities.remove(i)

    for dict in chapter_list:
        clean_student = {}
        for k,v in dict.items():
            if k in chapter_activities:
                if 'Completed' in str(v):
                    v = 'Completed'
                clean_student.update({k:v})
        p = percent_complete(clean_student)
        clean_student.update( {'Activities Complete': p[0]} )
        clean_student.update( {'Total Activities': p[1]} )
        clean_student.update( {'Percent Complete': p[2]} )

        clean_chapter.append(clean_student)

    return clean_chapter


# def match_name (dictionary):
#     record = dictionary
#     name = record['Name']
