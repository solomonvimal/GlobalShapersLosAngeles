#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 11:54:58 2021
@author: solo

#Setup Steps:
1. Go to https://api.slack.com/apps and create a new app
2. Go to OAuth & Permissions --> Scopes & set the scope. For the script here to work, atleast "chat:write" and/or "im:write" (not sure which one is critical) should be enabled.
3. Copy the Bot User OAuth Token which starts with xoxb-#################. 
4. Prepare a spreadsheet with columns "Shaper Name", "Slack ID", "Birthday". Slack UIDs can be quickly copy-pasted from the profiles. See here - https://stackoverflow.com/a/57538893/4383027
5. Download the script here, change the file path to the spreadsheet, edit column names if needed and modify the function "ping_people_to_wish" and "send_message_to_all" as needed.

#TODO:
1. Can directly link to google_sheet (https://docs.google.com/spreadsheets/d/xxxxxxx).
2. Can auto generate emails a few days before bdays using a scheduler.
3. Can customize messages (add emojis or so).
"""
import requests
import pandas as pd

# Things to change
df = pd.read_csv("/Users/solo/Desktop/Shapers_Celebrations/Shapers_directory.csv", skiprows=3, usecols = [i for i in range(3,12)])
slack_token =  # slack access bot token
bday_person="FirstName LastName"
presently_link="http://getpresently.com/c/card/?event=XXXXXXX"

def ping_people_to_wish(presently_link, bday_person):
    df_folks_to_ping = df[~df["Shaper Name"].isin([bday_person])]
    for i in range(len(df_folks_to_ping)):
        df_person = df_folks_to_ping.iloc[i]
        first_name, last_name = df_person["Shaper Name"].split(" ")
        UID = df_person["Slack ID"]
        bday = df[df["Shaper Name"]==bday_person]["Birthday"].values[0]
        message = "Hi " + first_name + ", \n" + bday_person.split(" ")[0] + \
                    "'s bday is coming up and we made a Presently link here: " + presently_link + \
                        ".\n We will send this to them by the end of day on " + bday + \
                            ". Would be great if you get a few moments to leave a message here by then."
        data = {'token': slack_token, 'channel': UID, 'as_user': True, 'text': message}
        requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    return

def ask_for_bday():        
    for i in range(len(df)):
        df_person = df.iloc[i]
        first_name, last_name = df_person["Shaper Name"].split(" ")[0:2]
        UID = df_person["Slack ID"]
        bday = df.iloc[i]["Birthday"]
        if not type(bday)==type("text"):
            print(first_name)    
            message = "Hi " + first_name + ", \n We do not have your bday in our Shapers Directory." + \
            " Could you please send us your birth day to Solomon? \n Thanks, \n Celebrations Team"
            data = {'token': slack_token, 'channel': UID, 'as_user': True, 'text': message}
            requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    return
            
def send_message_to_all(message):        
    for i in range(len(df)):
        df_person = df.iloc[i]
        first_name, last_name = df_person["Shaper Name"].split(" ")[0:2]
        UID = df_person["Slack ID"]
        message = "Hi " + first_name + ", \n Please ignore the previous message! It was meant to be sent to only a few folks." + \
                " If you receive a similar message after this one, then please send your bday to Solomon. Thanks!"
        data = {'token': slack_token, 'channel': UID, 'as_user': True, 'text': message}
        requests.post(url='https://slack.com/api/chat.postMessage', data=data)
    return
