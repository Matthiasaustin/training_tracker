import win32com.client as win32
import pandas as pd
import jinja2
import os


def get_message(recipient):
    name = str(recipient['first_name'])
    link = str(recipient['registration_link'])
    close_date = str(recipient['closing_date'])
    templateLoader = jinja2.FileSystemLoader(searchpath="../templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "email.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(name=name,  # Include args for render
                                 link=link,
                                 close_date=close_date)

    return outputText


# Currently windows only, may try to make system agnostic at somepoint
def make_email(recipient):
    print(recipient[0])
    print(recipient[1])
    recipient = recipient[1]
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    email = str(recipient['personal_email'])
    supervisor_email = str(recipient['sup_email'])

    mail.To = email
    mail.CC = supervisor_email
    text = get_message(recipient)
    subject = str(recipient['subject'])

    mail.Subject = subject
    mail.HtmlBody = text

    mail.Save()


# import_address
def import_info():
    PATH = os.path.abspath('../email_data')
    csv_name = 'cpr20210201.csv'
    PATH = os.path.join(PATH, csv_name)
    print(PATH)
    recipients = pd.read_csv(PATH)
    for row in recipients.iterrows():
        make_email(row)


if __name__ == "__main__":
    import_info()
