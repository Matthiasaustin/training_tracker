import pandas
import csv

print ('First Line')

# read in all the chapters completion status in csv
# For further dev: a faster way to pull the csvs and move them

c1 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_1.csv')
c2 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_2.csv')
c3 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_3.csv')
c4 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_4.csv')
c5 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_5.csv')
c6 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_6.csv')
c7 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_7.csv')
c8 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_8.csv')
c9 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_9.csv')
c10 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_10.csv')
c11 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_11.csv')
c12 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_12.csv')
c13 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_13.csv')
c14 = pandas.read_csv('~/Documents/code/training_tracker/data/progress.august_chapter_14.csv')

# convert dataframe to dictionaries
c1 = c1.to_dict('records')
c2 = c2.to_dict('records')
c3 = c3.to_dict('records')
c4 = c4.to_dict('records')
c5 = c5.to_dict('records')
c6 = c6.to_dict('records')
c7 = c7.to_dict('records')
c8 = c8.to_dict('records')
c9 = c9.to_dict('records')
c10 = c10.to_dict('records')
c11 = c11.to_dict('records')
c12 = c12.to_dict('records')
c13 = c13.to_dict('records')
c14 = c14.to_dict('records')

# List of all courses for iteration
courses = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14]

# Remove extra information
def clean_record(chap_comp_dict):
    """Removes extra information that is not necessary for current completion tracking and returns a list of dictionaries"""
    chapter = chap_comp_dict
    activities_01 = {key:value for key, value in chapter[0].items() if 'Complete' in str(value)}
    # clean_chapter = clean_chapter.keys()
    activities = ['Name', 'ID number', 'Institution', 'Email address']
    temp = list(activities_01.keys())
    for i in temp:
        activities.append(i)
    clean_chapter = []
    # for c in chapter:
    #     for key, v in c.items():
    #         if 'Completed' in str(c[key]):
    #             activities.append(key)

    for d in chapter:
        clean_student = {}
        for k,v in d.items():
            clean_student.update({'Name': d['Name']})
            clean_student.update({'ID number': d['ID number']})
            clean_student.update({'Institution': d['Institution']})
            clean_student.update({'Email address': d['Email address']})
            if k in activities:
                if 'Completed' in str(v):
                    v = 'Completed'
                clean_student.update({k:v})
        p = percent_complete(clean_student)
        clean_student.update( {'Activities Complete': p[0]} )
        clean_student.update( {'Total Activities': p[1]} )
        clean_student.update( {'Percent Complete': p[2]} )
        print(clean_student)
        clean_chapter.append(clean_student)
    return ( clean_chapter )
def percent_complete(student):
    """Takes a dictionary record of chapter completion for a student and returns total number of activities, total completed and percentage"""
    num_act = len( student.keys() )
    num_comp = 0
    for k,v in student.items():
        if 'Completed' in str(v):
            num_comp = num_comp + 1
    percent = int(100*( num_comp/( num_act - 4) ))
    return([num_comp,num_act,percent])
# Count total activities

# Count total activities completed

# Make percentage of completed activities
# Remove non-countable keys like name, id, etc.

def completion_report(list_of_c):
    """Takes a list of course records and makes a combined completion report for all students."""
# Stretch goal would be to write them to a single excel file and/or make a completion report based on the status
    clean_list = []
    for c in list_of_c:
        clean_list.append(clean_record(c))

def export_records (dict, export_location):
    """Exports the clean completion records to a csv file on disk"""
# Write all chapter's completion records to file


clean_record(c1)




# ***Boneyard***

# def course (name, activities):
#     """A structure for courses on Moodle to determine completion status quickly."""
#     activities = list(activities.keys())
#     print("This course is {}".format(name))
#     x=1
#     y = len(activities)
#     # print(y)
#     # print(activities:y])
#     chap_act = ['Name',]
#     while x<(y-4):
#         chap_act.append(activities[x])
#         x = x+2
#     return(chap_act)
# print(c1[1])

# def completion (c_dict, course):
#     # produces the headers for the csv file
#     course = course;
#     # is a list of dictionaries with students
#     students = c_dict;
#     comp_list=[]
#     for s in students:
#         student={}
#         student.update({'Name':s['Name']})
#         student.update({'ID number':s['ID number']})
#         student.update({'Email address':s['Email address']})
#         student.update({'Institution':s['Institution']})
#         for c in course:
#             v = s[c]
#             if 'Completed' in str(v):
#                 v = 'Completed'
#                 student.update({c:v})
#         comp = 0
#         for k , v in student.items():
#             if 'Completed' in str(v):
#                 comp = comp+1
#         student.update({'activities_completed': comp})   
#         student.update({'total_activities': ( len(course)-4 )})   
#         percent = int(100*(int(comp)/( len(course)-6 )))
#         student.update({'percentage_completed': percent})
#         comp_list.append(student)
#     # for s in students:
#     return(comp_list)
