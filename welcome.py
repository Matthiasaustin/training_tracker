import pandas
import csv

print ('First Line')
x = open('test.txt','a')
c1 = pandas.read_csv('~/Documents/code/training_tracker/data/completion-august_chapter_1-202008.csv')
c2 = pandas.read_csv('~/Documents/code/training_tracker/data/completion-august_chapter_2-20200813.csv')
c3 = pandas.read_csv('~/Documents/code/training_tracker/data/completion-august_chapter_3-20200813.csv')
c4 = pandas.read_csv('~/Documents/code/training_tracker/data/completion-august_chapter_4-20200813.csv')
# c5 = pandas.read_csv('')
# c6 = pandas.read_csv('')
# c7 = pandas.read_csv('')
# c8 = pandas.read_csv('')
# c9 = pandas.read_csv('')
# c10 = pandas.read_csv('')
# c11 = pandas.read_csv('')
# c12 = pandas.read_csv('')
c13 = pandas.read_csv('~/Documents/code/training_tracker/data/completion-august_chapter_13-202008.csv')
# c14 = pandas.read_csv('')

# convert dataframe to dictionaries
c1 = c1.to_dict('records')
c2 = c2.to_dict('records')
c3 = c3.to_dict('records')
c4 = c4.to_dict('records')
# c5 = c5.to_dict('records')
# c6 = c6.to_dict('records')
# c7 = c7.to_dict('records')
# c8 = c8.to_dict('records')
# c9 = c9.to_dict('records')
# c10 = c10.to_dict('records')
# c11 = c11.to_dict('records')
# c12 = c12.to_dict('records')
c13 = c13.to_dict('records')
# c14 = c14.to_dict('records')
classes = [c1, c2, c3, c4, c13]
headers = ['Name', 'C1 Status', 'C2 Status', 'C3 Status', 'C4 Status', 'C13 Status']
rows = []

# print(dict)
# print(dict[1])
# for rec in dict:
#     name = rec['Name']
#     x.write("Name: " + str(name)) 
#     if rec['Course complete'] is None or 'nan':
#         x.write(" | Chapter 13 Status: Incomplete")
#     else:
#         x.write("| Chapter 13 Status: " + str(rec['Course complete']))
#     x.write('\n---*---\n')

# for rec in dict:
#     name = rec['Name']
#     complete = rec['Course complete']
#     if complete is None or 'nan':
#         new_row = (name, "incomplete")
#     else:
#         new_row = (name, complete)
#     rows.append(new_row)
# print (rows)

# {student name: name, c1_status: x, ...}
def student (name, c1, c2, c3, c4, c13):
    '''Student object with status of completion by course over the first week'''
    name = name
    if c1 == 'nan':
        c1 = 'incomplete'
    if c2 == 'nan':
        c2 = 'incomplete'
    if c3 == 'nan':
        c3 = 'incomplete'
    if c4 == 'nan':
        c4 = 'incomplete'
    if c13 == 'nan':
        c13 = 'incomplete'

    c1_status = c1
    c2_status = c2
    c3_status = c3
    c4_status = c4
    c13_status = c13

    # return {name: name, c1: c1_status,c2: c2_status,c3: c3_status,c4: c4_status,c13: c13_status}
    return (name, c1_status, c2_status, c3_status, c4_status, c13_status)

students= []
x = 0
print(c1[0])
test = [sub['Course complete'] for sub in c1]
print ( test )
for student in c1:
    # trying to call the completion status by chapter and pair it once with the student's name, rather than have a bunch of copies
    c1_status =[sub['Course complete'] for sub in c1]
    c2_status =[sub['Course complete'] for sub in c2]
    c3_status =[sub['Course complete'] for sub in c3]
    c4_status =[sub['Course complete'] for sub in c4]
    c13_status =[sub['Course complete'] for sub in c13]

    new_student = student(student['Name'],c1_status,c2_status,c3_status,c4_status,c13_status)
    print(new_student)
    students.append(new_student)
    ++x
print(students)
for student in students:
        new_row = student()
        rows.append(new_row)
print (rows)
with open('test.csv', 'w') as fill:
    f_csv = csv.writer(fill)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
print("\nLast Line, file done\n")
x.close()
