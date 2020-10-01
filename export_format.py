"""
A program to format data given in either dictionary or dataframe and export an excel file.
"""
import pandas as pd
import csv
import xlsxwriter as xl
import datetime


# Open a writer, workbook and sheet
# TODO Pass the eventual function the name of the sheet/workbook to make
# workbook = xl.Workbook('test.xlsx')
# worksheet = workbook.add_worksheet()

writer = pd.ExcelWriter('pandas_test.xlsx', engine='xlsxwriter')


# read in a csv file to use as data
data = pd.read_csv('data/completion-september_chapter_01-20200918_1536-comma_separated.csv')

# test pandas writing function
data.to_excel(writer, sheet_name='Chapter 1')

workbook = writer.book
worksheet = writer.sheets['Chapter 1']


# Formats
start_date = datetime.datetime.strptime('2020-9-1', "%Y-%m-%d")
complete_format = workbook.add_format({'bg_color': '#90F685'})
started_format = workbook.add_format({'bg_color': '#F9E79F'})
incomplete_format = workbook.add_format({'bg_color': '#EDBB99 '})

worksheet.conditional_format('A2:C10', {'type': '3_color_scale'})
worksheet.conditional_format('A2:BG40', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'Completed',
                                         'format': complete_format})

worksheet.conditional_format('A2:BG40', {'type': 'text',
                                         'criteria': 'containing',
                                         'value': 'Not completed',
                                         'format': incomplete_format})

worksheet.conditional_format('A2:BG40', {'type': 'blanks',
                                         'format': incomplete_format})

worksheet.conditional_format('A2:BG40', {'type': 'date',
                                         'criteria': 'greater than',
                                         'value': start_date,
                                         'format': complete_format})

writer.save()
def dict_format(dictionary):

    return dictionary

def df_format(df):
    return df


if __name__ == '__main__':


    print("Formatting started")
    print("Formatting done")
