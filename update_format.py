import pandas as pd
import csv
import xlsxwriter as xl
import datetime


# Open a writer, workbook and sheet
# TODO Pass the eventual function the name of the sheet/workbook to make
# workbook = xl.Workbook('test.xlsx')
# worksheet = workbook.add_worksheet()



# Formats
class formats():
    def __init__(self,workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

        self.complete_format = workbook.add_format({'bg_color': '#90F685'})
        self.highlight_format = workbook.add_format({'bg_color': '#F4D03F'})
        self.started_format = workbook.add_format({'bg_color': '#F9E79F'})
        self.incomplete_format = workbook.add_format({'bg_color': '#EDBB99'})
        self.location = 'A2:BF100'

    def con_complete(self):
        return {'type': 'text',
                'criteria': 'containing',
                'value': 'Finished',
                'format': self.complete_format}

    def con_notstarted(self):
        return {'type': 'text',
                'criteria': 'containing',
                'value': 'Not Started',
                'format': self.incomplete_format}

    def con_blanks(self):
        blanks = {'type': 'blanks', 'format': self.incomplete_format}
        return blanks

    def con_started(self):
        return {'type': 'text',
                'criteria': 'containing',
                'value': 'Started',
                'format': self.started_format}

    def date(self):
        return {'type': 'time_period',
                'criteria': 'last 7 days',
                'format': self.highlight_format}

def dict_format(dictionary):
    return dictionary

def df_format(df):
    return df

def report_writer(df):
    date = datetime.datetime.date(datetime.datetime.now())
    print(date)
    # create a writer to save the formatted report with the date to excel
    writer = pd.ExcelWriter('formated_report_{}.xlsx'.format(date), engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Status Update {}'.format(date))
    workbook = writer.book
    worksheet = writer.sheets['Status Update {}'.format(date)]
    format = formats(workbook,worksheet)

    complete = format.con_complete()

    worksheet.conditional_format(format.location, format.con_blanks())
    worksheet.conditional_format(format.location, format.date())
    worksheet.conditional_format(format.location,format.con_complete())
    worksheet.conditional_format(format.location,format.con_notstarted())
    worksheet.conditional_format(format.location,format.con_started())


    writer.save()
    

if __name__ == '__main__':


    print("Formatting started")
    print("Formatting done")
