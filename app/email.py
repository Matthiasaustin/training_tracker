import win32com.client as win32
import pandas as pd
import jinja2
import os
import glob


def get_message(recipient, message_type):
    message_type = message_type
    templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    if message_type == 'cpr':
        name = str(recipient['first_name'])
        link = str(recipient['registration_link'])
        close_date = str(recipient['closing_date'])
        TEMPLATE_FILE = 'cpr_email.html'
        
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(name=name,  # Include args for render
                                     link=link,
                                     close_date=close_date)
    if message_type == '40hr':
        TEMPLATE_FILE = 'welcome_40hr.html'
        name = str(recipient['firstname'])
        month = "February"
        username = str(recipient['username'])
        password = str(recipient['password'])
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(name=name,  # Include args for render
                                     month=month,
                                     username=username,
                                     password=password)

    return outputText


# Currently windows only, may try to make system agnostic at somepoint
def make_email(recipient, subject, message_type):
    print(recipient[0])
    print(recipient[1])
    attachment = None
    subject = subject
    message_type = message_type
    recipient = recipient[1]
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    print(message_type)
    if message_type == "cpr":
        print('borked')
        email = str(recipient['personal_email'])
        supervisor_email = str(recipient['sup_email'])
    elif message_type == '40hr':
        email = str(recipient['email'])
        supervisor_email = str(recipient['profile_field_supervisor_email'])
        attachment = PATH = os.path.abspath("../email_data/attachments/feb_2021_syllabus.pdf")

    mail.To = email
    mail.CC = supervisor_email
    text = get_message(recipient, message_type)
    subject = str(subject)

    mail.Subject = subject
    if attachment != None:
        mail.Attachments.Add(Source=attachment)
    mail.HtmlBody = text

    mail.Save()


# import_address
def import_info():

    PATH = os.path.abspath('../email_data/send_info/')
    csv_name = 'feb_new_user_import.csv'
    joined = os.path.join(PATH,"*.csv")
    files = glob.glob(joined)
    # print(files)
    for f in files:
        print(f)

    csv_name= input("What file to use? - Use the full name after the last \\ \n")
    PATH = os.path.join(PATH, csv_name)
    print(PATH)
    message_type = input("40hr or cpr?\n")
    recipients = pd.read_csv(PATH)
    subject = input("What is the message subject?\n")
    for row in recipients.iterrows():
        make_email(row, subject, message_type)


if __name__ == "__main__":
    import_info()
