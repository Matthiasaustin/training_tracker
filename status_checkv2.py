import pandas
import csv
import os
import glob
import sys
import re

print("Check has started.")

# Read all csv completion reports into the program.
# Further dev includes faster way to access the information.

def import_data ():
    chapters = []
    ch_num = 1
    PATH = os.path.expanduser("~/*Documents/*code/*training_tracker/*data")
    EXT = "*.csv"
    joined = os.path.join(PATH,EXT)
    globbed = glob.glob(joined)
    # print(globbed)
    # chapters["c0"] = 0
    for c in globbed:
        print(c)
        print("***")
        ch_number = re.search("chapter_\d\d", c)
        ch_number = ch_number.group()
        print(ch_number)
        new_csv = pandas.read_csv(c)
        new_csv.fillna('Not Complete', inplace=True)
        # for k,v in new_csv:
                # new_csv[k].fillna('Not Complete', inplace=True)
        new_csv = new_csv.to_dict('records')

        for k in new_csv:
            k["Chapter"] = ch_number
        chapters.append(new_csv)
        ch_num += 1
    return chapters

def process_chapter(chapter):
    """ Takes the list of chapter data and processes them to clean the data and make it meaningful."""
    # Takes a chapter dictionary to process
    chapterX = chapter

    # keep the first six values: ID, Name, ID number, Email address, Department, Institution
    # Remove if there is "Completion Date" in key.

    # Read all key values from the dict
    chapterX_act = list(chapterX[0].keys())
    clean_act_list = []
    # Remove all "Date complete" headers from the list
    for i in chapterX_act:
        if "Completion date" not in str(i):
            clean_act_list.append(i)

    # create clean chapter from remaining values

    clean_chapter = []
    for d in chapterX:
        clean_student = {}
        for k,v in d.items():
            # clean_student.update({'Name': d['Name']})
            # clean_student.update({'ID number': d['ID number']})
            # clean_student.update({'Institution': d['Institution']})
            # clean_student.update({'Email address': d['Email address']})
            if k in clean_act_list:
                if 'Completed' in str(v):
                    v = 'Completed'
                clean_student.update({k:v})
        p = percent_complete(clean_student)
        clean_student.update( {'Activities Complete': p[0]} )
        clean_student.update( {'Total Activities': p[1]} )
        clean_student.update( {'Percent Complete': p[2]} )
        # print(clean_student)
        clean_chapter.append(clean_student)

    # Check the number of activities total, create percentage of activities completed

    # Check complete or not, highlight nearly completes >80%

    return clean_chapter

def percent_complete(student):
    """Takes a dictionary record of chapter completion for a student and returns total number of activities, total completed and percentage"""
    doc = 9
    new_docs = {'chapter_01':10, 'chapter_02':9, 'chapter_03':9,
'chapter_04':9, 'chapter_05':9,'chapter_06':9,'chapter_07':9,'chapter_08':9,'chapter_09':9,'chapter_10':9, 'chapter_11':9, 'chapter_12':9, 'chapter_13':9,'chapter_14':9}
    doc = new_docs[student['Chapter']]
    num_act = len( student.keys() ) - doc
    num_comp = 0
    for k,v in student.items():
        if 'Completed' in str(v):
            num_comp = num_comp + 1
    percent = int(100*( num_comp/num_act))
    return([num_comp,num_act,percent])
# Count total activities

# Count total activities completed

# Make percentage of completed activities
# Remove non-countable keys like name, id, etc.

def print_var_name(variable):
 for name in globals():
     if eval(name) == variable:
        print (name)


def test_prog ():
    chapters = import_data()
    test_chapter = chapters[0]
    processed_chapter = process_chapter(test_chapter)
    return processed_chapter
# print (test_prog ())
# Main Program with all parts
def main_program ():
    final_list = []
    chapters = import_data()
    for chapter in chapters:
        final_list.append(process_chapter(chapter))
    x=1
    final_list = make_report(final_list)
    for d in final_list:
        chapter = d[0]['Chapter']
        # headers = d.keys()
        pandas.DataFrame(d).to_csv('status_update{}.csv'.format("_"+str(chapter)), header=True, index=False)
        x = x+1
    print("Check Complete.")

def make_report (chapter_list):
    chapter_list = chapter_list
    br_ch_list = []

    for chapter in chapter_list:
        # make new chapter version
        ch_brief = []
        # get name, id number, percent complete, actual complete and chapter number,maybe chapter quiz
        for i in chapter:
            name = i['Name']
            department = i['Department']
            institution = i['Institution']
            id_number = i['ID number']
            percent = i['Percent Complete']
            if i['Course complete'] == 'Not Complete':
                complete = "Incomplete"
            else:
                complete = 'Finished'
            checked = i['Teacher']
            quiz = 'Incomplete'
            chapter = i['Chapter']
            st_brief = {'id_number': id_number, 'name': name, 'department': department,'percent_complete': percent, 'complete?': complete, 'chapter': chapter}
            ch_brief.append(st_brief)
        br_ch_list.append(ch_brief)

        # new list to hold the compilation of dictionaries to make into a table
        new_report = []

        # dictionary of names created already to check against, including the name and its list position
        names = {}

        # check each dict list in the br_ch list
        for d in br_ch_list:
            for i in d:
                if i['name'] in names:
                    print("Name Exists")
                    new_report.append(i)
                else:
                    names[i['name']] = True
                    for dict in new_report:
                        if dict['name'] == i['name']:
                            dict.update(i)

            # check each dictionary in the dict list
            # check name against list of names previously collected
            # if not any(names[e['name']] == e['name'] for e in names):
            #     print ("Name added")
            #     new_name = e['name']
            #     new_entry = {new_name:True}
            #     names.update(new_entry)
            # if name exists, add attributes to that dictionary
            # else:
            #     print('name exists')
    print(names)
    print(new_report)
    chapter_list.append(new_report)
    return chapter_list
                # if the name doesn't exist, add name and attributes as new dictionary


if __name__ == "__main__":

    main_program()
