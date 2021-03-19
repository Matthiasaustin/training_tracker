"""
Main program of the training reporter suite. The program onces complete will serve as the hub and "ui" through cli for various programs/modules for compiling reports and emailing staff/students
"""
import pandas as pd
import os
import glob
import shutil
from datetime import datetime
import app.data as data
import app.report_maker as report_maker
import app.email as email


def main_program():
    """Provides cli ui and menu/logic forking to direct the user and provide results"""

    # Test Area for proof of concept run

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    # Need to add relative paths to data, export and downloads here to there
    # aren't conflicts on local program runs. Add arguments for any function
    # that locates files and add to local/global run times.
    #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    get_csv = input("get new csv? y/n \n")
    if get_csv.lower() == "y":
        data.get_csv()
    input("press any key when finished")
    data_dir = os.path.abspath("data/")
    export_dir = os.path.abspath("export/")
    date = datetime.now().strftime("%Y%m%d")

    # make a directory for the data from today
    try:
        os.mkdir(f"data/Data{date}")
    except FileExistsError:
        pass
    rerun = "yes"
    while rerun == "yes":
        # assign archive folder
        archive = os.path.abspath(f"data/Data{date}")

        # download_dir = os.path.abspath("/home/matthias/Downloads")
        download_dir = os.path.abspath("c:/Users/maustin/Downloads")
        downloads = os.path.join(download_dir, "completion-*")
        files = glob.glob(downloads)
        months = []
        for f in files:
            months.append(data.get_month(f))
            months = list(set(months))

        for month in months:
            csv = data.import_data(month, data_dir, download_dir)
            records = report_maker.parse_data(csv)
            data.export_to_excel(records)
            PATH = os.path.join(os.path.abspath("data"), "*.csv")
            files = glob.glob(PATH)
            for f in files:
                shutil.move(f, archive)
        rerun = input("Rerun? yes or no\n").lower()

    # data.export_as_csv(x)
    # *************************************************

    # initial prompt and welcome

    # list options for tasks

    # take input and intiate tasks

    # prompt for more tasks or exit (on loop)

    # *************************************************
    # get_csv

    # for loop to move by month

    # run, format and export each, maybe combine


def run_single_report():
    data_dir = os.path.abspath("data/")
    export_dir = os.path.abspath("export/")
    date = datetime.now().strftime("%Y%m%d")
    download_dir = os.path.abspath("c:/Users/maustin/Downloads")
    downloads = os.path.join(download_dir, "completion-*")
    files = glob.glob(downloads)
    months = []
    # month = input("Month?\n").lower()
    month = "february"
    print(month)
    csv = data.import_data(month, data_dir, download_dir)
    records = report_maker.parse_data(csv)
    data.export_to_excel(records)
    PATH = os.path.join(os.path.abspath("data"), "*.csv")
    files = glob.glob(PATH)
    move = input("Move to archive? y/n\n")
    archive = os.path.abspath(f"data/Data{date}")
    if move.lower() == "y":
        for f in files:
            shutil.move(f, archive)
    email.import_info("mar_new_user_import.csv","freminder")


if __name__ == "__main__":

    print("Welcome to Trainer Hub['working title']")
    main_program()
    # run_single_report()
