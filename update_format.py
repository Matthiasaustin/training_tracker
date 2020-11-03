import pandas as pd
import csv
import xlsxwriter as xl
import datetime
import os, sys, glob
from pathlib import Path


# Open a writer, workbook and sheet
# TODO Pass the eventual function the name of the sheet/workbook to make
# workbook = xl.Workbook('test.xlsx')
# worksheet = workbook.add_worksheet()

PATH = os.path.expanduser("~/Documents/!Matthias/code/training_reporter/export")
date = datetime.datetime.date(datetime.datetime.now())
start_date = datetime.datetime.date(datetime.datetime.strptime("2020-9-30", "%Y-%m-%d"))
release_2 = start_date + datetime.timedelta(days=7)
release_3 = start_date + datetime.timedelta(days=14)

joined = os.path.join(PATH, f"status_update_{date}.xlsx")
print(joined)
joined = Path(joined)

# Formats
class formats:
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

        self.complete_format = workbook.add_format({"bg_color": "#90F685"})

        self.stale_format = workbook.add_format({"bg_color": "#82E0AA", "bold": 1})
        self.closed_format = workbook.add_format({'bg_color': '#F2F4F4', 'font_color': '#F2F4F4','pattern':1})
        self.not_enrolled= workbook.add_format({'bg_color': '#F2F4F4', 'font_color': '#F2F4F2','pattern':1})
        self.highlight_format = workbook.add_format(
            {
                "bold": 1,
                "bg_color": "#58D68D",
                "border": 6,
                "border_color": "red",
                "align": "center",
                "valign": "center",
            }
        )

        self.started_format = workbook.add_format({"bg_color": "#F9E79F"})
        self.incomplete_format = workbook.add_format({"bg_color": "#EDBB99"})
        self.not_enrolled = workbook.add_format(
            {"bg_color": "#F2F4F4", "font_color": "#F2F4F2", "pattern": 1}
        )
        self.location = "A5:BF100"

    def con_closed1(self):
        return {
            "type": "formula",
            "criteria": '=ISNUMBER(SEARCH("Closed",$O$2)) ',
            "value": "Closed",
            "format": self.closed_format,
        }

    def con_closed2(self):
        return {
            "type": "formula",
            "criteria": '=ISNUMBER(SEARCH("Closed",$V$2)) ',
            "value": "Closed",
            "format": self.closed_format,
        }

    def con_notenrolled(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Not Enrolled",
            "format": self.not_enrolled,
        }
        self.complete_format = workbook.add_format({'bg_color': '#90F685'})

        self.stale_format = workbook.add_format({'bg_color': '#82E0AA', 'bold': 1})
        self.highlight_format = workbook.add_format({'bold': 1,'bg_color': '#58D68D','border': 6, 'border_color': 'red','align':'center', 'valign':'center'})

        self.started_format = workbook.add_format({'bg_color': '#F9E79F'})
        self.incomplete_format = workbook.add_format({'bg_color': '#EDBB99'})
        self.location = 'A5:BF100'

    def con_complete(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Finished",
            "format": self.complete_format,
        }

    def con_notstarted(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Not Started",
            "format": self.incomplete_format,
        }

    def con_blanks(self):
        blanks = {"type": "blanks", "format": self.incomplete_format}
        return blanks

    def con_started(self):
        return {
            "type": "text",
            "criteria": "containing",
            "value": "Started",
            "format": self.started_format,
        }

    def date(self):
        return {
            "type": "time_period",
            "criteria": "last 7 days",
            "format": self.highlight_format,
        }

    def stale_date(self):
        return {
            "type": "date",
            "criteria": "less than",
            "value": datetime.datetime.now(),
            "format": self.stale_format,
        }


def dict_format(dictionary):
    return dictionary


def df_format(df):
    return df


def report_writer(df, start_date):
    start_date = start_date
    release_2 = start_date + datetime.timedelta(days=7)
    release_3 = start_date + datetime.timedelta(days=14)
    print("Todays Date:" + str(date) + "\nCourse Start Date:" + str(start_date))
    # create a writer to save the formatted report with the date to excel
    writer = pd.ExcelWriter(joined, engine="xlsxwriter")
    df = df.reindex(
        columns=[
            "Department",
            "Name",
            "Institution",
            "ID Number",
            "Chapter",
            "Completion Date chapter_01",
            "Completion Date chapter_02",
            "Completion Date chapter_03",
            "Due Date #1",
            "Completion Date chapter_04",
            "Completion Date chapter_13",
            "Completion Date chapter_14",
            "Due Date #2",
            "Completion Date chapter_05",
            "Completion Date chapter_06",
            "Completion Date chapter_07",
            "Due Date #3",
            "Completion Date chapter_08",
            "Completion Date chapter_11",
            "Due Date #4",
            "Completion Date chapter_09",
            "Completion Date chapter_10",
            "Completion Date chapter_12",
            "Due Date #5",
            "Chapter 12 Skills Lab",
            "Total Hours Completed",
            "Total Hours Outstanding",
        ]
    )
    df.rename(columns = {
            "Chapter": "Report(Y/N)",
            "Completion Date chapter_01": "Chapter 1",
            "Completion Date chapter_02": "Chapter 2",
            "Completion Date chapter_03": "Chapter 3",
            "Completion Date chapter_04": "Chapter 4",
            "Completion Date chapter_13": "Chapter 13",
            "Completion Date chapter_14": "Chapter 14",
            "Completion Date chapter_05": "Chapter 5",
            "Completion Date chapter_06": "Chapter 6",
            "Completion Date chapter_07": "Chapter 7",
            "Completion Date chapter_08": "Chapter 8",
            "Completion Date chapter_11": "Chapter 11",
            "Completion Date chapter_09": "Chapter 9",
            "Completion Date chapter_10": "Chapter 10",
            "Completion Date chapter_12": "Chapter 12",
    }, inplace=True)
    df.to_excel(writer, sheet_name="Status Update {}".format(date), startrow=3)
    workbook = writer.book

    worksheet = writer.sheets["Status Update {}".format(date)]
    set_1 = ["$G1:$N1", "$G2:$N2"]
    set_2 = ["$O1:$U1", "$O2:$U2"]
    set_3 = ["$V1:$Y1", "$V2:$Y2"]
    header_format = workbook.add_format(
        {
            "align": "center",
            "bold": True,
            "valign": "center",
            "bg_color": "#F2F4F4",
            "left": 1,
            "right": 1,
            "top":1,
        }
    )
    header_format2 = workbook.add_format(
        {
            "align": "center",
            "bold": True,
            "valign": "center",
            "bg_color": "#F2F4F4",
        }
    )

    worksheet.conditional_format("A1:AA3", {"type": "blanks", "format": header_format2})
    worksheet.conditional_format(
        "A1:AA3", {"type": "no_blanks", "format": header_format2}
    )

    worksheet.merge_range(
        set_1[0], f'Set #1 - Opened {start_date.strftime("%m/%d/%Y")}', header_format
    )
    worksheet.merge_range(
        set_2[0], f'Set #2 - Opened {release_2.strftime("%m/%d/%Y")}', header_format
    )
    worksheet.merge_range(
        set_3[0], f'Set #3 - Opened {release_3.strftime("%m/%d/%Y")}', header_format
    )
    dates = [start_date, release_2, release_3]
    status = []
    for d in dates:
        if d <= date:
            status.append("Open")
        else:
            status.append("Closed")

    worksheet.merge_range(set_1[1], f"These courses are: {status[0]}", header_format)
    worksheet.merge_range(set_2[1], f"These courses are: {status[1]}", header_format)
    worksheet.merge_range(set_3[1], f"These courses are: {status[2]}", header_format)

    duedate1 = release_2
    duedate2 = release_2 + datetime.timedelta(days=2)
    duedate3 = release_3
    duedate4 = release_3 + datetime.timedelta(days=2)
    duedate5 = release_3 + datetime.timedelta(days=14)

    worksheet.write("E3", "Estimated hours to complete:", header_format)
    worksheet.write("G3", "2.5hr", header_format)
    worksheet.write("H3", "2hr", header_format)
    worksheet.write("I3", "2.5hr", header_format)
    worksheet.write("J3", f'Due Date: {duedate1.strftime("%m/%d/%Y")}', header_format)
    worksheet.write("K3", "4hr", header_format)
    worksheet.write("L3", "1.5hr", header_format)
    worksheet.write("M3", "2hr", header_format)
    worksheet.write("N3", f'Due Date: {duedate2.strftime("%m/%d/%Y")}', header_format)
    worksheet.write("O3", "4hr", header_format)
    worksheet.write("P3", "1.5hr", header_format)
    worksheet.write("Q3", "2hr", header_format)
    worksheet.write("R3", f'Due Date: {duedate3.strftime("%m/%d/%Y")}', header_format)
    worksheet.write("S3", "4hr", header_format)
    worksheet.write("T3", "3hr", header_format)
    worksheet.write("U3", f'Due Date: {duedate4.strftime("%m/%d/%Y")}', header_format)
    worksheet.write("V3", "4hr", header_format)
    worksheet.write("W3", "2.5hr", header_format)
    worksheet.write("X3", "6hr", header_format)
    worksheet.write("Y3", f'Due Date: {duedate5.strftime("%m/%d/%Y")}', header_format)
    worksheet.write("Z3", "2hr", header_format)
    format = formats(workbook, worksheet)

    complete = format.con_complete()

    worksheet.conditional_format("$O5:$U100", format.con_closed1())
    worksheet.conditional_format("$V5:$Z100", format.con_closed2())
    worksheet.conditional_format(format.location, format.con_blanks())
    worksheet.conditional_format(format.location, format.date())
    worksheet.conditional_format(format.location, format.con_complete())
    worksheet.conditional_format(format.location, format.con_notstarted())
    worksheet.conditional_format(format.location, format.con_started())
    worksheet.conditional_format(format.location, format.stale_date())

    writer.save()


if __name__ == "__main__":

    print("Formatting started")
    print("Formatting done")
