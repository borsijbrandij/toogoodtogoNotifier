#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import getpass
from tgtg_requests import send_request
from notify_run import Notify
from tgtg_io import (
    check_notify_files_exist,
    check_tokens_exist,
    get_tokens_from_file,
    save_notify_run_settings,
    save_tokens_to_file,
    get_notify_run_channel_disk,
)
import os
import json


def get_notify_run_channel():
    """
    Check if notify run channel has been setup, if not create one.
    Returns a Notify object.

    """
    if os.path.isfile("./data/notify_channel.txt"):
        return get_notify_run_channel_disk()
    else:
        return setup_notify_run()


def setup_notify_run():
    """
    Function to create a new notify-run channel.
    Returns the endpoint URL.
    """
    # Setup notify run channel and print info
    notify = Notify()
    notify.register()
    print(notify.info())

    # Save channel endpoint to file
    save_notify_run_settings(notify)

    return notify.endpoint


def login(email, pw):
    """
    Sends username and pw to tgtg API.
    Returns Succes boolean and
    """
    data = (
        '{{"device_type": "ANDROID", "email": "{email}" , "password": "{pw}" }}'.format(
            email=email, pw=pw
        )
    )

    response, code = send_request(data=data)
    if code == 200:
        success = True
        save_tokens_to_file(response)

    else:
        print(response)
        success = False
    return success


def first_setup():
    """
    Function that gets called when launching program for the first time.
    Asks user for credentials and calls login function.
    """
    if not check_tokens_exist():
        print("You have not logged in yet. Please enter your credentials")
        time.sleep(0.2)
        email = input("Enter email: ")
        pw = getpass.getpass()

        # Try repeatedly logging in.
        while not login(email, pw):
            print("Incorrect credentials, let's try again")
            email = input("Enter email: ")
            pw = getpass.getpass()
