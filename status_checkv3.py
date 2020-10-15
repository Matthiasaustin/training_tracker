"""A program that reads chapter records, parses and combines the records to create
   a report which is formatted for send off to supervisory staff."""

import pandas
import csv
import os
import glob
import sys
import re
import chapter_format
import datetime
import update_format


def import_data():
    chapters = []
    ch_num = []

    # The general path to the fold that holds the data
    # PATH = os.path.expanduser("~/*Documents/*code/*training_tracker/*data")

    PATH = os.path.expanduser("~/*Documents/*!Matthias/*code/*training_reporter/*data")
    # what type of files are read in
    EXT = "*.csv"

    # joins the path to folder to the extension
    joined = os.path.join(PATH, EXT)

    # creates a list of specific locations to read from the path and extension
    globbed = glob.glob(joined)

    # Sorts the list for easier handling later
    globbed.sort()

    # for each of the paths in the new list, capture the chapter number and
    # import the csv
    for c in globbed:
        # match chapter number and add it to the chapter number list
        ch_number = re.search("chapter_\d\d", c)
        ch_number = ch_number.group()
        print(ch_number)

        # read in the csv file as a pandas dataframe
        new_csv = pandas.read_csv(c)

        # fill in any empy cells with "Incomplete"
        new_csv.fillna("Incomplete", inplace=True)

        # converts the datafram to a dictionary
        new_csv = new_csv.to_dict("records")

        # adds the chapter number to each dictionary for future reference
        for k in new_csv:
            k["Chapter"] = ch_number

        # adds the list of student records in dict form to a list of chapters
        chapters.append(new_csv)

        # adds chapter number to list of chapters imported
        ch_num.append(ch_number)

    # returns the list of chapters (each a list of dictionary),
    # and list of chapter numbers for reference
    return_list = [chapters, ch_num]

    return return_list


def make_report(chapter_list):

    # assigns the master list of chapters
    chapter_list = chapter_list

    # creates a holding list for the refined master list
    new_chapter_list = []

    # new report record to add to the master chapter list
    report = []

    # list of names with T/F to check if they've been encountered before
    names = {}

    for chapter in chapter_list:
        chapter = chapter_format.clean_data(chapter)
        for record in chapter:
            complete = "Default"
            completion_date = "Not Started"
            # the information in k,v for the student in the report list

            name = record["Name"]

            if record["Course complete"] == "Incomplete":
                if record["Percent Complete"] >= 1:
                    complete = "Started"
                    completion_date = "Started"
                else:
                    complete = "Not Started"
                    completion_date = "Not Started"
            else:
                complete = "Finished"
                completion_date = datetime.datetime.strptime(
                    record["Course complete"], "%d/%m/%y, %H:%M"
                )
                completion_date = completion_date.date()

            if name not in names:
                names[name] = True
                report.append(
                    {
                        "Name": record["Name"],
                        "Department": record["Department"],
                        "Institution": record["Institution"],
                        "ID Number": record["ID number"],
                        # 'Percent {}'.format(record['Chapter']): record['Percent Complete'],
                        "Complete {}".format(record["Chapter"]): complete,
                        "Chapter": "Report",
                        "Completion Date {}".format(record["Chapter"]): completion_date,
                    }
                )
            else:
                for i in report:
                    if i["Name"] == record["Name"]:
                        i.update(
                            {
                                "Name": record["Name"],
                                "Department": record["Department"],
                                "Institution": record["Institution"],
                                "ID Number": record["ID number"],
                                # 'Percent {}'.format(record['Chapter']): record['Percent Complete'],
                                "Complete {}".format(record["Chapter"]): complete,
                                "Chapter": "Report",
                                "Completion Date {}".format(
                                    record["Chapter"]
                                ): completion_date,
                            }
                        )

    print(
        "******************************\nCourse Start Date: YYYY-MM-DD\n******************************"
    )
    start_date = datetime.datetime.strptime(input(), "%Y-%m-%d")
    # start_date= datetime.strptime('2020-9-25', '%Y-%m-%d')
    start_date = datetime.datetime.date(start_date)
    for s in report:
        s = chapter_format.hour_checker(s, start_date)
    return report


def export_data(dict_list):
    print("Exporting")
    df_list = []
    date = datetime.datetime.date(datetime.datetime.now())
    for d in dict_list:
        print(d[0]["Chapter"])
        chapter = d[0]["Chapter"]
        now = datetime.datetime.now()
        df = pandas.DataFrame(d)
        df_list.append(df)

    for df in df_list:
        if df.loc[2, "Chapter"] == "Report":
            df.fillna("Not Enrolled", inplace=True)
            update_format.report_writer(df)


def main_program():
    data = import_data()
    chapters = data[0]
    chapter_list = data[1]
    chapter_list = chapter_list.sort()
    final_list = [chapter for chapter in chapters]

    report = make_report(chapters)
    final_list.append(report)

    export_data(final_list)
    print("Finished")


if __name__ == "__main__":

    print("Check has started.")
    main_program()
