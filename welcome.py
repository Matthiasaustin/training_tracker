import pandas
import csv

print ('First Line')
x = open('test.txt','a')
f = pandas.read_csv('~/Documents/code/training_tracker/data/aug_c13_comp.csv')

print(f.loc[0:10,"Name":"Course complete"])
print("----")
print(f.loc[0:,"Name":"Course complete"])
students = []
dict = f.to_dict('records')
headers = ['Name', 'C13 Status']
rows = []
# print(dict)
# print(dict[1])
for rec in dict:
    name = rec['Name']
    x.write("Name: " + str(name)) 
    if rec['Course complete'] is None or 'nan':
        x.write(" | Chapter 13 Status: Incomplete")
    else:
        x.write("| Chapter 13 Status: " + str(rec['Course complete']))
    x.write('\n---*---\n')
for rec in dict:
    name = rec['Name']
    complete = rec['Course complete']
    if complete is None or 'nan':
        new_row = (name, "incomplete")
    else:
        new_row = (name, complete)
    rows.append(new_row)
print (rows)

with open('test.csv', 'w') as fill:
    f_csv = csv.writer(fill)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
print("\nLast Line, file done\n")
x.close()
