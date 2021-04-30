import os
from tgtg_setup import first_setup
from tgtg_io import check_tokens_exist, get_user_id_from_file
from tgtg_requests import get_fav_items, get_new_items, send_to_notify_run
from tgtg_setup import get_notify_run_channel
import time


def start_listening():
    """
    Function that gets called after initialization is done.
    Repeatedly queries tgtg server and checks for new magic boxes.
    Sends push notification when new magic box from user's favourites is available.
    """
    # Print info
    print("Starting listening...")
    notify_run_endpoint = get_notify_run_channel()
    print(
        "Reminder, you can subscribe for notifications at: "
        + str(notify_run_endpoint[0])
    )
    user_id = get_user_id_from_file()

    # Setup variables
    starttime = time.time()
    notify = get_notify_run_channel()

    old_items = {}

    # Repeatedly check for new items every 15 seconds
    while True:
        current_items = get_fav_items(user_id)
        new_items = get_new_items(old_items, current_items)

        # When new magic boxes are available, send notification with notify-run
        if new_items:
            send_to_notify_run(new_items, notify)

        # Wait 15 seconds before sending new query to server
        time.sleep(15.0 - ((time.time() - starttime) % 15.0))

        old_items = current_items


def main():
    if not check_tokens_exist():
        first_setup()

    start_listening()


main()
