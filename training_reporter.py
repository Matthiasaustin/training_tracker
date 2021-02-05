"""
Main program of the training reporter suite. The program onces complete will serve as the hub and "ui" through cli for various programs/modules for compiling reports and emailing staff/students
"""
import app.data as data


def main_program():
    """Provides cli ui and menu/logic forking to direct the user and provide results"""

    # Test Area for proof of concept run
    df_list = data.import_data()

    # *************************************************

    # initial prompt and welcome

    # list options for tasks

    # take input and intiate tasks

    # prompt for more tasks or exit (on loop)


    # *************************************************
    # get_csv

    # for loop to move by month
    # run, format and export each, maybe combine

if __name__ == "__main__":

    print("Welcome to Trainer Hub['working title']")
    main_program()
