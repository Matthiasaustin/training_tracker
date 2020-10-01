""" Provides utilities to clean up the chapter records read in via CSV from Moodle courses """

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
