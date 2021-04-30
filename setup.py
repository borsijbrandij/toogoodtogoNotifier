import time
import getpass
from tgtg_requests import login


def first_setup():
    print("You have not logged in yet. Please enter your credentials")
    time.sleep(0.2)
    email = input("Enter email: ")
    pw = getpass.getpass()

    while not login(email, pw):
        print("Incorrect credentials, let's try again")
        email = input("Enter email: ")
        pw = getpass.getpass()
        
        


