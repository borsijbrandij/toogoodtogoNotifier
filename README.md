# Too Good to Go Notifier
Too Good to Go is an app where restaurants and shops can offer "magix boxes" with leftover items with high discounts. Because these magic boxes can be put online at any moment it can be usefull to get a notification when one of your favourite companies has new magic boxes are available. 

This python program that queries Too Good to Go servers to check if new magic-boxes are available. 
It only checks for magic boxes you have marked as favourite in the toogoodtogo app. These favourites are linked to your account.
Whenever one of your favourite magic boxes become available, a webpush notification will be sent to your devices using a notify-run channel.




# Requirements
- Too Good to Go account
- Python 3.9
- Requests 2.25.1 for sending HTTP requests (https://pypi.org/project/requests/)
- Notify-run 0.0.13 for sending webPush notifications (https://pypi.org/project/notify-run/)

# Instructions
Start program with
```
$ python ./main
```
First run
- It will ask for your toogoodtogo username and password 
- It generates a notify-run channel and prints the link. Subscribe to the channel with your device to receive notifications whenever one 
