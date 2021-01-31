"""
Imports and exports raw, unformatted data, handles paths
"""
import pandas as pd
import os, glob, sys, re
import datetime

# import app.format as format
# import report_maker


# import
def import_path():

    # PATH = os.path.expanduser("~/*Documents/*!Matthias/*code/*training_reporter/*data")
    # user_path = input("What path to your csv files? Type N for default\n")
    # if user_path == "N" or "n":
    #     user_path = "~/Documents/code/training_tracker/data"
    user_path = "~/Documents/code/training_tracker/data"

    PATH = os.path.expanduser(user_path)
    # what type of files are read in
    EXT = "*.csv"

    # joins the path to folder to the extension
    joined = os.path.join(PATH, EXT)

    # creates a list of specific locations to read from the path and extension
    path_list = glob.glob(joined)

    # Sorts the list for easier handling later
    path_list.sort()

    return path_list


def import_csvs(path_list):
    path_list = path_list
    imported_csv = []
    chapters_imported = []
    for file in path_list:
        month = re.search(r"-(.*?)_c", file)
        month = month.group()
        month = month.replace("-", "")
        month = month.replace("_c", "")
        month.strip()

        # reviews the path and pulls out the chapter numbers
        chapter_number = re.search("chapter_\d\d", file)
        chapter_number = chapter_number.group()

        # reads the csv file in as a dataframe, fills any missing values with incomplete
        new_csv = pd.read_csv(file, parse_dates=["Course complete"], dayfirst=True)
        new_csv.fillna("Incomplete", inplace=True)

        new_csv["Chapter"] = chapter_number
        new_csv["Month"] = month

        imported_csv.append(new_csv)
        chapters_imported.append(chapter_number)

    return imported_csv


def import_data():
    path_list = import_path()
    dataframes = import_csvs(path_list)

    return dataframes


# export
# def export(list_df):
# db import/export tbd
