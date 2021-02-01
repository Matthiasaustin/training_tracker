import jinja2
import os

# make_message
def get_message():
    templateLoader = jinja2.FileSystemLoader(searchpath="../templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "email.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    name = "Testing"
    outputText = template.render(name=name)  # this is where to put args to the template renderer

    return outputText

def make_email():
# import_address

# import_message


if __name__ == "__main__"
