import pandas as pd
import csv
import xlsxwriter as xl
import datetime


# Open a writer, workbook and sheet
# TODO Pass the eventual function the name of the sheet/workbook to make
# workbook = xl.Workbook('test.xlsx')
# worksheet = workbook.add_worksheet()


# Formats
class formats:
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

        self.complete_format = workbook.add_format({"bg_color": "#90F685"})

        self.stale_format = workbook.add_format({"bg_color": "#82E0AA", "bold": 1})
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
        self.location = "A2:BF100"

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


def report_writer(df):
    date = datetime.datetime.date(datetime.datetime.now())
    columns_titles = ['Name','Department', 'Institution', 'ID Number','Chapter',
                      'Completion Date chapter_01',
                      'Completion Date chapter_02',
                      'Completion Date chapter_03',
                      'Completion Date chapter_04',
                      'Completion Date chapter_13',
                      'Completion Date chapter_14',
                      'Set 1 Hours Completed',
                      'Completion Date chapter_05',
                      'Completion Date chapter_06',
                      'Completion Date chapter_07',
                      'Completion Date chapter_08',
                      'Completion Date chapter_11',
                      'Set 2 Hours Completed',
                      'Completion Date chapter_09',
                      'Completion Date chapter_10',
                      'Completion Date chapter_12',
                      'Set 3 Hours Completed',
                      'Total Hours Completed',
                      'Total Hours Outstanding'
                      ]
    
    print(date)
    # create a writer to save the formatted report with the date to excel
    writer = pd.ExcelWriter("formated_report_{}.xlsx".format(date), engine="xlsxwriter")
    df = df.reindex(columns=columns_titles)
    df.to_excel(writer, sheet_name="Status Update {}".format(date))
    workbook = writer.book
    worksheet = writer.sheets["Status Update {}".format(date)]
    format = formats(workbook, worksheet)

    complete = format.con_complete()

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
