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
from app.export_format import prep_df, formats

today = datetime.datetime.date(datetime.datetime.now())


def grade_courses():
    try:
        course_id_df = pd.read_csv("../course_id.csv")
    except Exception:
        course_id_df = pd.read_csv("course_id.csv")
    course_ids = course_id_df.loc[:, "id"]
    # url.request.urlretrieve(csv_url, data_dir+"test.csv")

    for k, v in course_ids.items():
        course_id = str(v)
        url = f"https://dstrainings.com/report/completion/index.php?course={course_id}"
        webbrowser.open(url, autoraise=False)


def make_date(one_date):
    # one_date = str(one_date)
    # one_date = datetime.datetime.strptime(one_date,'%Y-%m-%d')
    new_date = datetime.datetime.date(one_date)
    return new_date


# import app.format as format
# import report_maker
def get_csv():
    try:
        course_id_df = pd.read_csv("../course_id.csv")
    except Exception:
        course_id_df = pd.read_csv("course_id.csv")
    course_ids = course_id_df.loc[:, "id"]
    # url.request.urlretrieve(csv_url, data_dir+"test.csv")

    for k, v in course_ids.items():
        course_id = str(v)
        csv_url = f"https://dstrainings.com/report/completion/index.php?course={course_id}&format=csv"
        # webbrowser.open(csv_url, autoraise=False)


# https://dstrainings.com/report/completion/index.php?course={course_id}&format=csv


def import_path(month, data_dir, download_dir):

    print(download_dir)
    downloads = os.path.join(download_dir, f"completion-{month}*")
    print(downloads)
    files = glob.glob(downloads)
    print(files)
    for f in files:
        shutil.move(f, data_dir)

    PATH = data_dir
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


def get_hours(ch_num):
    # chapter_hours =
    return {
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
    }.get(ch_num, 2)


def import_csvs(path_list):
    path_list = path_list
    imported_csv = []
    chapters_imported = []
    for file in path_list:
        # reviews the path and pulls out the chapter numbers
        chapter_number = re.search("chapter_\d\d", file)
        chapter_number = chapter_number.group()

        # reads the csv file in as a dataframe, fills any missing values with incomplete
        new_csv = pd.read_csv(file,
                              parse_dates=["Course complete"],
                              dayfirst=True)
        new_csv.fillna("Incomplete", inplace=True)
        month = get_month(file)
        new_csv["Chapter"] = chapter_number
        new_csv["Month"] = month

        imported_csv.append(new_csv)
        chapters_imported.append(chapter_number)

    return imported_csv


def import_data(month, data_dir, download_dir):
    path_list = import_path(month, data_dir, download_dir)
    dataframes = import_csvs(path_list)

    return dataframes


def clean_up():
    """Resets the data folder and archives files currently within prior to next run"""


# export
def export_as_csv(df, export_dir, style="institutions" ):

    df_list = df
    export_dir = export_dir
    dt = datetime.datetime.date(datetime.datetime.now())
    dt = datetime.datetime.strftime(dt, "%Y-%m-%d")
    if style == "insitutions":
        for d in df_list[1:]:
            if d["Instution"] != None:
                try:
                    institution = d.loc[0, "Institution"]
                    institution = institution.lower()
                    filename = f"{institution}_status_update_{dt}.csv"
                    export = os.path.join(export_dir, filename)
                    d.to_csv(export, index=False)
                except Exception:
                    print("Something is wrong in export_as_csv w/ Range")
    elif style == "combined":
        print("Printing Combined CSV")
        try:
            month = df_list.loc[0,"Month"]
            filename = f"{month.lower()}_combinded_update_{dt}.csv"
            export = os.path.join(export_dir,filename)
            df.to_csv(export, index=False)
        except Exception:
            raise Exception("Export combined CSV Failed.")

def export_to_excel(df_list):
    df_list = df_list

    # Gets month from course report and looks up recorded start date
    month = df_list[1].loc[0, "Month"]
    date = datetime.datetime.date(datetime.datetime.now())
    today = datetime.datetime.strftime(date, "%B%d-%Y")
    PATH = "course_start_dates.csv"

    course_dates = pd.read_csv(PATH)
    start_date = course_dates.loc[course_dates["cohort_month"] == month,
                                  "start_date"]
    start_date = datetime.datetime.strptime(str(start_date.item()), "%Y-%m-%d")
    start_date = datetime.datetime.date(start_date)

    release_2 = start_date + datetime.timedelta(days=7)
    release_3 = start_date + datetime.timedelta(days=14)

    dates = [start_date, release_2, release_3]

    prepped_df = []
    for df in df_list:
        n_df = prep_df(df)
        prepped_df.append(n_df)

    # creates writer for pd and xlswriter
    writer = pd.ExcelWriter(f"export/{month}_status_update_{date}.xlsx",
                            engine="xlsxwriter",
                            date_format="mm/dd/yy")
    month_t = month.title()
    sola_sheet = f"SOLA Update {date}"
    voa_sheet = f"VOA {month_t} Update {date}"
    try:
        first_institution = prepped_df[0].loc[0, "Institution"]
    except:
        if prepped_df[1].loc[0, "Institution"] == "VOAWW":
            first_institution = "SOLA"
        else:
            print("Only one institution listed, which did not participate?")
            institution = input()
    if first_institution == "VOAWW":
        prepped_df[0].to_excel(writer, sheet_name=voa_sheet, startrow=3)
        prepped_df[1].to_excel(writer, sheet_name=sola_sheet, startrow=3)
    if first_institution == "SOLA":
        prepped_df[1].to_excel(writer, sheet_name=voa_sheet, startrow=3)
        prepped_df[0].to_excel(writer, sheet_name=sola_sheet, startrow=3)

    workbook = writer.book
    sola_worksheet = writer.sheets[sola_sheet]
    voa_worksheet = writer.sheets[voa_sheet]
    worksheet_list = [sola_worksheet, voa_worksheet]
    for worksheet in worksheet_list:
        set_1 = ["$G1:$N1", "$G2:$N2"]
        set_2 = ["$O1:$U1", "$O2:$U2"]
        set_3 = ["$V1:$Y1", "$V2:$Y2"]

        header_format = workbook.add_format({
            "align": "center",
            "bold": True,
            "valign": "center",
            "bg_color": "#F2F4F4",
            "left": 1,
            "right": 1,
            "top": 1,
        })

        header_format2 = workbook.add_format({
            "align": "center",
            "bold": True,
            "valign": "center",
            "bg_color": "#F2F4F4",
        })

        worksheet.conditional_format("A1:AB3", {
            "type": "blanks",
            "format": header_format2
        })
        worksheet.conditional_format("A1:AB3", {
            "type": "no_blanks",
            "format": header_format2
        })
        # Merge and format header row
        worksheet.merge_range(
            set_1[0],
            f'Set #1 - Opened {start_date.strftime("%m/%d/%Y")}',
            header_format,
        )

        worksheet.merge_range(
            set_2[0], f'Set #2 - Opened {release_2.strftime("%m/%d/%Y")}',
            header_format)

        worksheet.merge_range(
            set_3[0], f'Set #3 - Opened {release_3.strftime("%m/%d/%Y")}',
            header_format)

        status = []
        for d in dates:
            # d = make_date(d)
            # date = make_date(date)
            if d <= date:
                status.append("Open")
            else:
                status.append("Closed")

        worksheet.merge_range(set_1[1], f"These courses are: {status[0]}",
                              header_format)
        worksheet.merge_range(set_2[1], f"These courses are: {status[1]}",
                              header_format)
        worksheet.merge_range(set_3[1], f"These courses are: {status[2]}",
                              header_format)

        duedate1 = release_2
        duedate2 = release_2 + datetime.timedelta(days=2)
        duedate3 = release_3
        duedate4 = release_3 + datetime.timedelta(days=2)
        duedate5 = release_3 + datetime.timedelta(days=14)

        # TODO Check Alignment
        worksheet.write("E3", "Estimated hours to complete:", header_format)
        worksheet.write("G3", "2.5hr", header_format)
        worksheet.write("H3", "2hr", header_format)
        worksheet.write("I3", "2.5hr", header_format)
        worksheet.write("J3", f'Due Date: {duedate1.strftime("%m/%d/%Y")}',
                        header_format)
        worksheet.write("K3", "4hr", header_format)
        worksheet.write("L3", "1.5hr", header_format)
        worksheet.write("M3", "2hr", header_format)
        worksheet.write("N3", f'Due Date: {duedate2.strftime("%m/%d/%Y")}',
                        header_format)
        worksheet.write("O3", "4hr", header_format)
        worksheet.write("P3", "1.5hr", header_format)
        worksheet.write("Q3", "2hr", header_format)
        worksheet.write("R3", f'Due Date: {duedate3.strftime("%m/%d/%Y")}',
                        header_format)
        worksheet.write("S3", "4hr", header_format)
        worksheet.write("T3", "3hr", header_format)
        worksheet.write("U3", f'Due Date: {duedate4.strftime("%m/%d/%Y")}',
                        header_format)
        worksheet.write("V3", "4hr", header_format)
        worksheet.write("W3", "2.5hr", header_format)
        worksheet.write("X3", "6hr", header_format)
        worksheet.write("Y3", f'Due Date: {duedate5.strftime("%m/%d/%Y")}',
                        header_format)
        worksheet.write("Z3", "2hr", header_format)
        format = formats(workbook, worksheet)

        worksheet.conditional_format("$O5:$U100", format.con_closed1())
        worksheet.conditional_format("$V5:$Z100", format.con_closed2())
        worksheet.conditional_format(format.location, format.con_blanks())
        worksheet.conditional_format(format.location, format.date())
        worksheet.conditional_format(format.location, format.con_complete())
        worksheet.conditional_format(format.location, format.con_notstarted())
        worksheet.conditional_format(format.location, format.con_started())
        worksheet.conditional_format(format.location, format.stale_date())

    writer.save()


# def export(list_df):
# db import/export tbd
if __name__ == "__main__":

    grade_courses()
    # if running from the sub folder app
    data_dir = os.path.abspath("../data")
    export_dir = os.path.abspath("../export")
    download_dir = os.path.abspath("/home/matthias/Downloads")
    downloads = os.path.join(download_dir, "completion-*")
    today = datetime.datetime.date(datetime.datetime.now())
