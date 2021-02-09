import win32com.client as win32
import pandas as pd
import jinja2
import os
import glob

class Message():
    def __init__(self, df_row):
        recipient = df_row[0]
        self.name = ""
        self.message_type = ""
        self.template = ""
        self.outputText = "None has been specified. Please run a constructor"

        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)

    def cpr_start_email():
        self.email = str(recipient['personal_email'])
        self.supervisor_email = str(recipient['sup_email'])
        self.attachement = None
        self.name = str(recipient['first_name'])
        self.link = str(recipient['registration_link'])
        self.close_date = str(recipient['closing_date'])
        self.template_file = 'cpr_email.html'
        template = templateEnv.get_template(template_file)
        outputText = template.render(self.name=name,  # Include args for render
                                     self.link=link,
                                     self.close_date=close_date)

    def fhr_start_email():
        self.email = str(recipient['email'])
        self.supervisor_email = str(recipient['profile_field_supervisor_email'])
        self.attachment = PATH = os.path.abspath("../email_data/attachments/feb_2021_syllabus.pdf")
        self.template_file = 'welcome_40hr.html'
        self.name = str(recipient['firstname'])
        self.month = "February"
        self.username = str(recipient['username'])
        self.password = str(recipient['password'])
        self.template = templateEnv.get_template(template_file)
        self.outputText = template.render(self.name=name,  # Include args for render
                                     self.month=month,
                                     self.username=username,
                                     self.password=password)

    def fhr_reminder_email():
        fhr_start_email()
        self.template_file = 'reminder_40hr.html'
        self.template = templateEnv.get_template(template_file)
        self.outputText = template.render(self.name=name,  # Include args for render
                                     self.month=month)
    def get_body():
        return self.outputText


def get_message(recipient, message_type):
    message_type = message_type
    templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)


# Currently windows only, may try to make system agnostic at somepoint
def make_email(recipient, subject, message_type):
    subject = subject
    message_type = message_type
    message = Message(recipient[1])
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    if message_type == 'cpr':
        message.cpr_start_email()
    elif message_type == 'fstart':
        message.fhr_start_email()
    elif message_type == 'freminder':
        message.fhr_reminder_email()

    mail.To = message.email
    mail.CC = message.supervisor_email
    text = message.get_body()
    subject = str(subject)

    mail.Subject = subject
    if message.attachment != None:
        mail.Attachments.Add(Source=message.attachment)
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
