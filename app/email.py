import win32com.client as win32
import pandas as pd
import jinja2
import os
import glob
from datetime import datetime, timedelta


class Message:
    def __init__(self, df_row):
        self.name = ""
        self.recipient = df_row
        self.message_type = ""
        self.attachment = None
        self.template = ""
        self.outputText = "None has been specified. Please run a constructor"

        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)

    def cpr_start_email(self):
        self.email = str(self.recipient["personal_email"])
        self.supervisor_email = str(self.recipient["sup_email"])
        self.attachment = None
        self.name = str(self.recipient["first_name"])
        self.link = str(self.recipient["registration_link"])
        self.close_date = str(self.recipient["closing_date"])
        self.template_file = "cpr_email.html"
        date = datetime.now()
        date = date.strftime("%m/%d/%Y")
        self.subject = f"CPR/First Aid Required - {date}"
        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(self.template_file)
        name = self.name
        link = self.link
        close_date = self.close_date
        self.outputText = template.render(
            name=name, link=link, close_date=close_date  # Include args for render
        )

    def fhr_start_email(self):
        self.email = str(self.recipient["email"])
        self.supervisor_email = str(self.recipient["profile_field_supervisor_email"])
        self.attachment = PATH = os.path.abspath(
            "../email_data/attachments/sola_mar_2021_syllabus.pdf"
        )
        self.template_file = "welcome_40hr.html"
        self.name = str(self.recipient["firstname"])
        self.month = "February"
        self.subject = f"Welcome to the {self.month} 40hr Core"
        self.username = str(self.recipient["username"])
        self.password = str(self.recipient["password"])
        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.template = templateEnv.get_template(self.template_file)
        name = self.name
        month = self.month
        username = self.username
        password = self.password
        self.outputText = self.template.render(
            name=name,  # Include args for render
            month=month,
            username=username,
            password=password,
        )

    def fhr_reminder_email(self):
        update_df = pd.read_csv("../export/feb_status_update_2021-02-19.csv")
        # update_info = update_df.loc[
        #     update_df["ID Number"] == self.recipient["idnumber"]
        # ]
        self.fhr_start_email()
        # start_date = datetime.date(
        #     datetime.strptime(self.recipient["hire_date"], "%Y-%m-%d")
        # )
        # days_left = (start_date + timedelta(days=120)) - datetime.now().date()
        # days_left = days_left.days
        date = datetime.now()
        date = date.strftime("%m/%d/%Y")
        self.subject = f"Training Reminder/Update - {date}"
        self.template_file = "reminder_40hr.html"
        # update_info = update_info.to_html()
        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        name = self.name
        month = self.month
        update_info = ""

        self.template = templateEnv.get_template(self.template_file)
        self.outputText = self.template.render(
            name=name,  # Include args for render
            month=month,
            # days_left=days_left,
            # update_info=update_info,
        )

    def get_body(self):
        return self.outputText


def get_update_info():
    """Temporary function til robust version incorporated"""


# Currently windows only, may try to make system agnostic at somepoint
def make_email(recipient, message_type):
    message_type = message_type
    message = Message(recipient[1])
    outlook = win32.Dispatch("outlook.application")
    mail = outlook.CreateItem(0)

    if message_type == "cpr":
        message.cpr_start_email()
    elif message_type == "fstart":
        message.fhr_start_email()
    elif message_type == "freminder":
        message.fhr_reminder_email()

    mail.To = message.email
    mail.CC = message.supervisor_email
    text = message.get_body()

    mail.Subject = message.subject
    if message.attachment != None:
        mail.Attachments.Add(Source=message.attachment)
    mail.HtmlBody = text

    mail.Save()


# import_address
def import_info():
    PATH = os.path.abspath("../email_data/send_info/")
    csv_name = "feb_new_user_import.csv"
    joined = os.path.join(PATH, "*.csv")
    files = glob.glob(joined)
    # print(files)
    for f in files:
        print(f)

    csv_name= input("What file to use? - Use the full name after the last \\ \n")
    PATH = os.path.join(PATH, csv_name)
    print(PATH)
    recipients = pd.read_csv(PATH)
    default_input_message = """
    Which would message?\n
    cpr\n
    fstart (40hr Welcome message)\n
    freminder (40hr Reminder message)\n
    """

    message_type = input(default_input_message)
    for recipient_row in recipients.iterrows():

        make_email(recipient_row, message_type)


if __name__ == "__main__":
    import_info()
