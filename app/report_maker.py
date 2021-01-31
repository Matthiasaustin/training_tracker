import pandas as pd
import numpy as np
import data
from datetime import datetime

# hour_checker

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
    new_cols = static_headers
    course = course_dataframe
    activities = list(course.columns[6:-7])
    course["Activities Completed"] = 0
    new_cols.append("Activities Completed")
    completion_dates = []
    for activity in activities:
        if "Completion date" in activity:
            course[activity] = pd.to_datetime(course[activity], dayfirst=True, errors='coerce')
            completion_dates.append(activity)
            new_cols.append(activity)
    for act in completion_dates:
        for i, r in course[act].items():
            if r is not pd.NaT:
                course.loc[int(i),'Activities Completed'] += 1
        # for i, r in course.iterrows():
            # print(r)
            # break

    num_activity = len(completion_dates)
    
    course_out = course[new_cols]
    rows = len(course_out.index)
    for i in range(0,int(rows)):
        if course_out.loc[i,"Activities Completed"] >= num_activity-1:
            course_out.loc[i,'Status'] = 'Complete'
        elif course_out.loc[i,'Activities Completed'] >= 1:
            course_out.loc[i,'Status'] = "Started"
        else:
            course_out['Status'] = "Not Started"

    print(course_out[['Name', 'Chapter', 'Activities Completed', 'Status']])

    return course_out

# parse_data
def parse_data(list_of_df):
    new_df_list = []
    class_records = list_of_df
    for course in class_records:
        static_headers = ['ID', 'Name', 'ID number', 'Email address', 'Department', 'Institution','Teacher', 'Manager','Course complete', 'Chapter', 'Month']
        new_df = check_started(course, static_headers)

        new_df_list.append(new_df)



    return new_df_list


# write_out

if __name__ == '__main__':
    csv = data.import_data()

    x = parse_data(csv)

