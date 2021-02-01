import pandas as pd
import numpy as np
import data
from datetime import datetime

# hour_checker

static_headers = ['ID', 'Name', 'ID number', 'Email address', 'Department', 'Institution','Teacher', 'Manager','Course complete', 'Chapter', 'Month']

chapter_hours = {
        "chapter_01": 2.5,
        "chapter_02": 2,
        "chapter_03": 2.5,
        "chapter_04": 4,
        "chapter_05": 4,
        "chapter_06": 1.5,
        "chapter_07": 2,
        "chapter_08": 4,
        "chapter_09": 4,
        "chapter_10": 2.5,
        "chapter_11": 2.5,
        "chapter_12": 6,
        "chapter_13": 1.5,
        "chapter_14": 2,
    }

# percent_check


# clean_data
def check_started(course_dataframe, static_headers):

    new_cols = static_headers  # columns that will definitely go into output
    course = course_dataframe
    activities = list(course.columns[6:-5])  # excludes known columns at beginning and end of file
    course["Activities Completed"] = 0  # sets default value for new col
    new_cols.append("Activities Completed")  # adds new col to output list
    completion_dates = []  # empty list to add cols with "completion date" in heading
    # completion date heading is a filter for activities students can complete

    for activity in activities:
        if "Completion date" in activity:
            # all "completion date" cols have a date if finished. Else NaT (not a date)

            course[activity] = pd.to_datetime(course[activity], dayfirst=True, errors='coerce')  

            completion_dates.append(activity)  # Add activity title to list
            # new_cols.append(activity)  # Add activity to final course df list *May remove

    for act in completion_dates:  # for every activity listed, loop through
        for i, r in course[act].items():  # get index and row for the items w/ activity
            if r is not pd.NaT:  # if the activity has a date in the row (i.e. student finished)
                course.loc[int(i),'Activities Completed'] += 1  # increment completion count by 1

    num_activity = len(completion_dates)  # get total number of activities
    # print(new_cols)
    course_out = course.loc[:,new_cols]  # create new df with listed columns and all rows
    rows = len(course_out.index)  # determine total rows to loop over
    for i in range(0,int(rows)):  # loops over all rows
        act_comp = int(course_out.at[i,'Activities Completed'])  # how many act completed?
        comp_percent = int(100 * (act_comp / num_activity))
        if course_out.at[i, 'Course complete'] != "Incomplete":  # If course is marked complete, will have a date, otherwise noted as "incomplete"

            course_out.loc[i,'Status'] = course_out.at[i, 'Course complete']
        elif act_comp >= 1:  # if they have completed one or more activities they have started the course
            course_out.loc[i,'Status'] = f"Started({comp_percent}%)"
        else:
            course_out.loc[i,'Status'] = "Not Started"

    # print(course_out[['Name', 'Chapter', 'Activities Completed', 'Status','Course complete']])
    # print("\n*****\n")

    return course_out


def combine_report(df_list):
    df_list = df_list
    report = pd.DataFrame
    report = df_list[0].loc[:, :]
    chapters = {'chapter_01': "Chapter 1",
                'chapter_02': "Chapter 2",
                'chapter_03': "Chapter 3",
                'chapter_04': "Chapter 4",
                'chapter_05': "Chapter 5",
                'chapter_06': "Chapter 6",
                'chapter_07': "Chapter 7",
                'chapter_08': "Chapter 8",
                'chapter_09': "Chapter 9",
                'chapter_10': "Chapter 10",
                'chapter_11': "Chapter 11",
                'chapter_12': "Chapter 12",
                'chapter_13': "Chapter 13",
                'chapter_14': "Chapter 14"}

    for df in df_list:
        ch_in = df.loc[0, 'Chapter']
        chapter_col = chapters[ch_in]
        df[chapter_col] = df.loc[:, 'Status']
        rows = len(df.index)
        for r in range(0, rows):
            name = df.loc[r,"Name"]
            print(name)
            if name in df.values:
                print(True)
            if name in report.values and name != None:
                print(name)
                # index = report[report['Name' == name]].index.values
                print(report['Name'])
                print(report.query('Name' == name))
                print(report.iloc[name].index)
                print(report.index[report['Name' == name]].to_list())
                print(report['Name' == name].index)
                print(report['Name' == name].index.to_list())
                index = report['Name' == name].index.to_list()
                report.loc[index, chapter_col] = df.loc[r, chapter_col]
            if name not in report.values:
                report = report.append(df.loc[r, :])

    print(report)


def parse_data(list_of_df):
    new_df_list = []
    class_records = list_of_df
    for course in class_records:

        static_headers = ['ID', 'Name', 'ID number', 'Email address', 'Department', 'Institution','Teacher', 'Manager','Course complete', 'Chapter', 'Month']
        new_df = check_started(course, static_headers)
        new_df_list.append(new_df)

    new_df_list = combine_report(new_df_list)

    return new_df_list


# write_out

if __name__ == '__main__':
    csv = data.import_data()
    x = parse_data(csv)
