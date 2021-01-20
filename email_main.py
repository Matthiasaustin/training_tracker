import pandas
import sys
import os

def message (df):

    df = df[1]
    name = str(df['first_name'])
    full_name = str(df['first_name']) + " " + str(df['last_name'])
    print(name)
    email_1 = df['personal_email']
    email_2 = df['sup_email']
    subject = f"VOAWW Training Notification: {full_name} CPR/First Aid Due"
    line_one = f"Hello {name},\n\n"
    line_two = "You're receiving this message because you need to complete a CPR/First Aid course. At the moment we can only offer an online version to meet this requirement. You can find more details below:\n"
    line_three = "\nHere is the link to a short tutorial video that will walk you through the initial process of getting started.\n"
    youtube_link = "https://youtu.be/Y6p6NVo7d4c"

    line_four = f"\nLink: {youtube_link}\n"
    line_five = "\nBelow is the link needed to register for the course, as well as the date the course will be closed. All progress must be finished by that date or will need to be restarted."
    line_six = f"\n\nRegistration link: {df['registration_link']}\n"
    line_seven = f"Closing Date: {df['closing_date']} \n"
    line_eight = "\nIf you have a CPR/First Aid certificate from another organization, or any immediate questions about this requirement, please contact your program manager. They have been made aware of this requirement, have been cc'd on this message and will be following up with you about it."
    line_nine = "\n\nThis is a vital requirement of your position and failure to complete on time may result in being removed from assigned work shifts for health and safety."
    line_ten = "\n\nPlease reach out with any questions,"
    print(line_nine)
    f = open("cpr_email.txt", "a")
    f.write ("\n\n\n\n*****\n\n\n\n" +
             str(email_1) +
             "\n\n" +
             str(email_2) +
             "\n\n" +
             str( subject ) +
             "\n\n-----\n\n" +
             str(line_one)   +
             str(line_two)    +
             str(line_three)  +
             str(line_four)   +
             str(line_five)   +
             str(line_six)    +
             str(line_seven)  +
             str(line_eight)  +
             str(line_nine)   +
             str(line_ten)
    )
    f.close()



def make_message(dataframe):
    """Takes dataframe of data from csv read in during main and uses that and other inputs to create a message draft in outlook via html markup."""
    df = dataframe

    # define subject line

    # indicate to and cc emails

    # path to attachments

    # message to use

    # template fields and matching columns from df

    # show example of first formated message for accept or restart

    # create messages as drafts (at least until reliable, then add option for direct send)

def main_program():
    csv_file_path = input("What is the path to the csv file you want to use?")
    PATH = os.path.expanduser("~/Documents/!Matthias/projects/")
    # import csv
    staff_list = pandas.read_csv(PATH)
    # print(staff_list)
    # convert to df

    # pass to the message formatter
    for row in staff_list.iterrows():
        message(row)
    # add message to list
    # write list to text file


if __name__ == "__main__":

    print("Check has started.")
    main_program()
