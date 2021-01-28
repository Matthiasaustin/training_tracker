import pandas as pd
import data

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

# parse_data
def parse_data(list_of_df):
    new_df_list = []
    class_records = list_of_df
    for course in class_records:
        course['Status'] = 'Not Started'
        if 
        new_df = course[['Institution', 'Department', 'Name', 'ID number','Chapter','Course complete']]
        print(course.iloc[0])
        new_df_list.append(new_df)

    
    
    return new_df_list


# write_out

if __name__ == '__main__':
    csv = data.import_data()
    x = parse_data(csv)

