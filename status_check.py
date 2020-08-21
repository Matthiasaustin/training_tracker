import pandas
import csv

# add in a reader function that takes in csv data and converts nan to "incomplete"
print ('First Line')

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

courses = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14]

def course (name, activities):
    """A structure for courses on Moodle to determine completion status quickly."""
    activities = list(activities.keys())
    print("This course is {}".format(name))
    x=1
    y = len(activities)
    # print(y)
    # print(activities:y])
    chap_act = ['Name',]
    while x<(y-4):
        chap_act.append(activities[x])
        x = x+2
    return(chap_act)
# print(c1[1])

def completion (c_dict, course):
    # produces the headers for the csv file
    course = course;
    # is a list of dictionaries with students
    students = c_dict;
    comp_list=[]
    for s in students:
        student={}
        for c in course:
            v = s[c]
            if 'Completed' in str(v):
                v = 'Completed'
                student.update({c:v})
        comp = 0
        for k , v in student.items():
            if 'Completed' in str(v):
                comp = comp+1
        student.update({'activities_completed': comp})   
        student.update({'total_activities': ( len(course)-4 )})   
        percent = int(100*(int(comp)/( len(course)-6 )))
        student.update({'percentage_completed': percent})
        comp_list.append(student)
    # for s in students:
    return(comp_list)

def dict2csv(dictlist, csvfile):
    """
    Takes a list of dictionaries as input and outputs a CSV file.
    """
    f = open(csvfile, 'wb')

    fieldnames = dictlist[0].keys()

    csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
    csvwriter.writerow(dict((fn, fn) for fn in fieldnames))
    for row in dictlist:
        csvwriter.writerow(row)
    fn.close()

c1_comp = completion(c1, course("Chapter 1", c1[0]))
print(c1_comp[0])
print(c2[0])
c2_comp = completion(c2, course("Chapter 2", c2[0]))
print(c2_comp[4])
