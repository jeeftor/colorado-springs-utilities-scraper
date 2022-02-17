"""Parsing Functions"""
from enum import Enum

from bs4 import BeautifulSoup


def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)
    action = form.attrs.get("action")
    if action:
        action = action.lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value = input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    for select in form.find_all("select"):
        # get the name attribute
        select_name = select.attrs.get("name")
        # set the type as select
        select_type = "select"
        select_text = select.text
        select_options = []
        option_texts = []
        # the default select value
        select_default_value = ""
        # iterate over options and get the value of each
        for select_option in select.find_all("option"):
            # get the option value used to submit the form
            option_text = select_option.text
            option_texts.append(option_text)
            option_value = select_option.attrs.get("value")
            if option_value:
                select_options.append(option_value)
                if select_option.attrs.get("selected"):
                    # if 'selected' attribute is set, set this option as default
                    select_default_value = option_value
        if not select_default_value and select_options:
            # if the default is not set, and there are options, take the first option as default
            select_default_value = select_options[0]
        # add the select to the inputs list
        inputs.append({"type": select_type, "text": select_text, "name": select_name, "values": select_options,
                       "options": option_texts,
                       "value": select_default_value})
    for textarea in form.find_all("textarea"):
        # get the name attribute
        textarea_name = textarea.attrs.get("name")
        # set the type as textarea
        textarea_type = "textarea"
        # get the textarea value
        textarea_value = textarea.attrs.get("value", "")
        # add the textarea to the inputs list
        inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})

    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


class MeterType(Enum):
    ELECTRIC_GENERATED = 1
    ELECTRIC_USED = 2
    WATER_USED = 3
    GAS_USED = 4


def make_form_data(html, meter: MeterType = None):
    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")
    details = get_form_details(forms[0])

    data = {}
    for input_tag in details["inputs"]:
        if input_tag["type"] == "hidden":
            # if it's hidden, use the default value
            data[input_tag["name"]] = input_tag["value"]
        elif input_tag["type"] == "text":
            data[input_tag["name"]] = input_tag["value"]
        else:
            print(input_tag)

    # Download commnad
    data['ctl00$ContentPlaceHolder1$UI_ExternalUserControl1$btnCsv'] = 'Download Spreadsheet Data'
    # Gas Meter
    data['ctl00$ContentPlaceHolder1$UI_ExternalUserControl1$dlLocationID'] = 'N:2646052025:NN'
    return data
