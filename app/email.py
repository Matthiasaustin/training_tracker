import win32com.client as win32
import pandas as pd
import jinja2
import os
import glob
import re
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
            "../email_data/attachments/mar_2021_syllabus.pdf"
        )
        self.template_file = "welcome_40hr.html"
        self.name = str(self.recipient["firstname"])
        self.month = "March"
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
        update_path = os.path.abspath("../email_data/send_info/march_combined_update.csv")
        update_df = pd.read_csv(update_path)
        update_info = update_df.loc[
            update_df["Email address"] == self.recipient["email"]
        ]
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
        update_info = update_info.loc(axis=1)["Chapter 1",
                                       "Chapter 2",
                                       "Chapter 3",
                                       "Chapter 4",
                                       "Chapter 5",
                                       "Chapter 6",
                                       "Chapter 7",
                                       "Chapter 8",
                                       "Chapter 9",
                                       "Chapter 10",
                                       "Chapter 11",
                                       "Chapter 12",
                                       "Chapter 13",
                                       "Chapter 14"]
        update_info = update_info.transpose().to_html()
        update_info = re.sub("<td>Not Started","<td style=\"background: orange;\">Not Started",update_info)
        update_info = re.sub("<td>Started","<td style=\"background: yellow;\">Started",update_info)
        update_info = re.sub("<td>\d.*:\d\d","<td style=\"background: green;\">Finished<\/td>",update_info)
        update_info = re.sub("th>\d<\/th|th>\d\d<\/th","th>Status<\/th", update_info)
        update_info = re.sub("th><\/th","th>Chapter<\/th",update_info)
        self.template = templateEnv.get_template(self.template_file)
        self.outputText = self.template.render(
            name=name,  # Include args for render
            month=month,
            # days_left=days_left,
            update_info=update_info,
        )

    def peer_coaching(self):
        self.email = str(self.recipient["email"])
        self.supervisor_email = str(self.recipient["profile_field_supervisor_email"])
        self.attachment = PATH = os.path.abspath(
            "../email_data/attachments/virtual_peer_coaching_handouts.pdf"
        )
        self.template_file = "peer_coaching.html"
        self.name = str(self.recipient["firstname"])
        self.month = "March"
        self.subject = f"March Virtual Peer Coaching Class Information"
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
    def peer_coaching_reminder(self):
        self.email = str(self.recipient["email"])
        self.supervisor_email = str(self.recipient["profile_field_supervisor_email"])
        self.template_file = "peer_coaching_reminder.html"
        self.name = str(self.recipient["firstname"])
        self.month = "March"
        self.subject = f"Reminder: March Virtual Peer Coaching Class"
        templateLoader = jinja2.FileSystemLoader(searchpath="../email_data/templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.template = templateEnv.get_template(self.template_file)
        name = self.name
        month = self.month
        self.outputText = self.template.render(
            name=name,  # Include args for render
            month=month,
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
    elif message_type == "peer":
        message.peer_coaching()
    elif message_type == "peerR":
        message.peer_coaching_reminder()

    mail.To = message.email
    mail.CC = message.supervisor_email
    text = message.get_body()

    mail.Subject = message.subject
    if message.attachment != None:
        mail.Attachments.Add(Source=message.attachment)
    mail.HtmlBody = text

    mail.Save()


# import_address
def import_info(message_type=None, csv_name=None):
    PATH = os.path.abspath("../email_data/send_info/")
    csv_name = "mar_new_user_import.csv"
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
    * cpr
    * fstart (40hr Welcome message)
    * freminder (40hr Reminder message)
    * peer (Peer Coaching)
    * peerR (Peer Coaching Reminder #1)
    \n
    """

    message_type = input(default_input_message)
    for recipient_row in recipients.iterrows():

        make_email(recipient_row, message_type)


if __name__ == "__main__":
    import_info()
