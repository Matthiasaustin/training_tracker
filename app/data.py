"""
Imports and exports raw, unformatted data, handles paths
"""
import pandas as pd
import os, glob, sys, re
import datetime
import webbrowser
import urllib as url
# import requests
import shutil

data_dir = os.path.abspath("../data")
export_dir = os.path.abspath("../export")
download_dir = os.path.abspath("/home/matthias/Downloads")
downloads = os.path.join(download_dir,'completion-*')
# import app.format as format
# import report_maker
def get_csv():
    PATH = "../course_id.csv"
    course_id_df = pd.read_csv(PATH,)
    course_ids = course_id_df.loc[:,'id']
    # url.request.urlretrieve(csv_url, data_dir+"test.csv")

    for k,v in course_ids.items():
        course_id = str(v)
        csv_url = f"https://dstrainings.com/report/completion/index.php?course={course_id}&format=csv"
        print(csv_url)
        # webbrowser.open(csv_url, autoraise=False)

    files = glob.glob(downloads)

    for file in files:
        shutil.move(file,data_dir)

# https://dstrainings.com/report/completion/index.php?course={course_id}&format=csv
# import
def import_path():

    # PATH = os.path.expanduser("~/*Documents/*!Matthias/*code/*training_reporter/*data")
    # user_path = input("What path to your csv files? Type N for default\n")
    # if user_path == "N" or "n":
    #     user_path = "~/Documents/code/training_tracker/data"
    user_path = "../data/"

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

def get_month(file_path):
    file = file_path
    month = re.search(r"-(.*?)_c", file)
    month = month.group()
    month = month.replace("-", "")
    month = month.replace("_c", "")
    month.strip()

    return month

def import_csvs(path_list):
    path_list = path_list
    imported_csv = []
    chapters_imported = []
    for file in path_list:
        # reviews the path and pulls out the chapter numbers
        chapter_number = re.search("chapter_\d\d", file)
        chapter_number = chapter_number.group()

        # reads the csv file in as a dataframe, fills any missing values with incomplete
        new_csv = pd.read_csv(file, parse_dates=["Course complete"], dayfirst=True)
        new_csv.fillna("Incomplete", inplace=True)
        month = get_month(file)
        new_csv["Chapter"] = chapter_number
        new_csv["Month"] = month

        imported_csv.append(new_csv)
        chapters_imported.append(chapter_number)

    return imported_csv


def import_data():
    get_csv()
    path_list = import_path()
    dataframes = import_csvs(path_list)

    return dataframes

def clean_up():
    """Resets the data folder and archives files currently within prior to next run"""
# export
# def export(list_df):
# db import/export tbd
if __name__ == "__main__":
    import_data()
