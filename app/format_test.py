import pandas as pd
from datetime import datetime
import os
import data


def main():
    df_list = data.import_data()
    df = df_list[0]
    excel_export(df)


def excel_export(df):
    df = df
    writer = pd.ExcelWriter("../export/test.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Test1", startrow=3)
    df.to_excel(writer, sheet_name="Test2")
    # writer.save()


if __name__ == "__main__":
    main()
