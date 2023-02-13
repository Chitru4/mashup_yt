# Mashup Module by Chitraksh Kumar

## Description
This module creates a mashup of songs of your favorite singer with a few steps from the command line.
Select the singer, the number of songs and there durations and you will get a mashup of their most popular hits.
The app might take a bit long to run due to downloading of multiple files from the net.

## Requirements
``` 
pip install pytube
pip install pydub
pip install requests
pip install flask
```

## Install
Download the code using pip
```
pip install mashup_yt
```

## Running the code
Before running code make sure to add your smtp google account as well as it's app password.
The password would be a 16 character string.
This step is not needed if you intend to use only the cli interface and not the web app.
```
mashup_yt -p example@gmail.com secret_password
```
```
mashup_yt "Marshmello" 20 20 out.mp3
mashup_yt -w
```

## Using the web app
A sendgrid account and api key is necessary to run the webapp as intended.
Navigate to the webapp folder and change email and api according to your needs in app.py.
After that enter the below command on the terminal.
```
set FLASK_APP=app.py  
flask run
mashup_yt -w
```

The app should run and provide you with a link which can be opened to run the mashup webapp.
Enter the required entries and the given email id should recieve a zip file containing the desired audio file.
Errors most likely might occur due to wrong from email mentioned in app.py or incorrect api key.
Make sure mashup.py is in the same folder as app.py

webpage can be changed by editing the php code in templates named index.html

The webapp can be hosted online on a platform like heroku or pythonanywhere.com for free.

## My Website
[Mashup-yt](http://chitru4.pythonanywhere.com/)
