#!/usr/bin/env python3

import argparse
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = 'https://www.googleapis.com/auth/calendar'
service = None
UTC_OFFSET = ':00-07:00'

CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "credentials.json")
TOKEN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "token.pickle")


def initialize():
    """
    Initialize the connection to the google calendar API
    :return: None
    """
    global service

    creds = None

    # if the directory of the script contains toke.pickle
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


def insert_event(summary, start, end, notifications):
    """
    Insert the event into Google Calendar
    :param summary: Summary of the event ie the title
    :param start: Start time of the event
    :param end: End time of the event
    :param notifications: How often reminders are sent corresponding
    :return: None
    """
    event = {
        'summary': summary,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles'
        },
        'reminders': {
            'useDefault': False,
            'overrides': notifications
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(event.get('htmlLink'))


def get_notification_priority(priority):
    """
    Get how often reminders should be sent through Google Calendar Poups
    :param priority: The priority of the event (high, normal, none)
    :return: How often reminders will be sent high = 5 days in adv, normal = 3 days in adv, none = no notifications
    """
    if priority == 'high':
        # Popups 5 days in advance
        notifications = [
            {'method': 'popup', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 48 * 60},
            {'method': 'popup', 'minutes': 72 * 60},
            {'method': 'popup', 'minutes': 96 * 60},
            {'method': 'popup', 'minutes': 120 * 60}]

        return notifications

    elif priority == 'normal':
        # Popups 3 days in advance
        notifications = [
            {'method': 'popup', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 48 * 60},
            {'method': 'popup', 'minutes': 72 * 60}]

        return notifications

    else:
        notifications = []

        return notifications


def parse():
    """
    Parse the arguments from the user and pass them to the insert_event function.
    End time is optional, if it is not supplied it will set the end time to the start time
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", help="The title of the calendar event")
    parser.add_argument("start", help="The start time of the calendar event, ex. 2019-02-20T11:00")
    parser.add_argument("priority", help="The priority of the notifications", choices=["high", "normal", "none"])
    parser.add_argument("--end", help="The end time of the calendar event, ex. 2019-02-20T11:00")
    args = parser.parse_args()

    start_time = args.start + UTC_OFFSET

    if args.end:
        end_time = args.end + UTC_OFFSET
    else:
        end_time = start_time

    reminder = get_notification_priority(args.priority)

    insert_event(summary=args.summary, start=start_time, end=end_time, notifications=reminder)


if __name__ == "__main__":
    initialize()
    parse()
