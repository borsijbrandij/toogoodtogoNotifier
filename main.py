import os
from setup import first_setup

def check_files_exist():
    return os.path.isfile('./data/tokens.json')

def start_server():
    print("starting server...")
    return


def main():
    if check_files_exist():
        start_server()
    else:
        first_setup()
    



    
main()