from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys
import zipfile
from flask import Flask, render_template_string, request, send_file
import requests
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer_name = request.form.get("singer_name")
        number_of_videos = int(request.form.get("number_of_videos"))
        duration_of_each_video = int(request.form.get("duration_of_each_video"))
        email = request.form.get("email")

        #mash(singer_name,number_of_videos,duration_of_each_video)
        
        with zipfile.ZipFile("videos.zip", "w") as zip:
            zip.write("out.mp3")

       
        send_email(singer_name, email, "videos.zip")

        return "Zip file sent successfully!"

    return render_template_string('''<html>
    <head>
        <title>Zip File Generator</title>
    </head>
    <body>
        <form method="post">
            <input type="text" name="singer_name" placeholder="Singer Name">
            <input type="text" name="number_of_videos" placeholder="Number of Videos">
            <input type="text" name="duration_of_each_video" placeholder="Duration of Each Video (in seconds)">
            <input type="email" name="email" placeholder="Email">
            <input type="submit" value="Submit">
        </form>
    </body>
</html>''')


def send_email(singer_name, to, zip_file):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    mail_content = '''
    Enjoy your mashup.
    '''
    # sender_address = 'example@gmail.com'
    # sender_pass = 'secret_password'
    password = open("pass.txt",'r')
    sender_address,sender_pass = map(str,password.read().split())
    print(sender_address,sender_pass)
    password.close()
    receiver_address = to
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Mashup of ' + str(singer_name)
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = zip_file
    with open(attach_file_name, 'rb') as attachment:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(attachment.read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment; filename="%s"' % zip_file)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def mash(x,n,y):
    delete_after_use = True

    x = x.replace(' ','') + "songs"
    try:
        n = int(n)
        y = int(y)
    except:
        sys.exit("Wrong Parameters entered")
    output_name = 'out.mp3'
        
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    vid_num = 0 
    i = 0 
    while i < n:
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[vid_num]) 
        print(yt.length)
        print("Downloading File "+str(i+1)+" .......")
        try: 
            mp4files = yt.streams.filter(only_audio=True).first().download(filename='tempaudio-'+str(i)+'.mp3')
        except:
            vid_num += 1
            continue
        i += 1
        vid_num += 1

    print("Files downloaded.")
    print("Getting the mashup ready.....")

    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/tempaudio-"+str(i)+".mp3"
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[0:y*1000],crossfade=1000)
  
    try:
        fin_sound.export(output_name, format="mp3")
        print("File downloaded successfuly. Stored as " + str(output_name))
    except:
        sys.exit("Error saving file. Try differrent file name")
        
    if delete_after_use:
        for i in range(n):
            os.remove("tempaudio-"+str(i)+".mp3")
            
def main():
    delete_after_use = True

    if len(sys.argv) < 2:
        sys.exit("No Parameters entered")

    if sys.argv[1] == '-w' or sys.argv[1] == '--web':
        app.run(host='0.0.0.0', port=5001)
        index()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("mashup_yt [options]:[-w --web web] [-h --host help] [-p --pass password] [no-options]:[4 arguments]")
        print("************************************************************************")
        print('''Before running code make sure to add your smtp google account as well as it's app password.
                 The password would be a 16 character string.
                 This step is not needed if you intend to use only the cli interface and not the web app.
                 mashup_yt -p example@gmail.com secret_password''')
        print("-w : Activate webapp, open the given address in a web-browser. Does not take additional arguments")
        print("-h : open the help page. Does not take additional arguments")
        print("-p : set the account id and password for smtp. Takes 2 additional arguments: 1.email-id 2.app-password")
        print("For help on how to generate app password search google")
        print("If no arguments are given cli will be used and it expects 4 arguments")
        print("1.Singer-name 2.Number of videos 3.Length of each video 4.Output file name(Enter absolute path)")
        sys.exit()
    elif sys.argv[1] == '-p' or sys.argv[1] == '-pass':
        password = open("pass.txt",'w')
        password.write(str(sys.argv[2])+' '+str(sys.argv[3]))
        password.close()
        sys.exit()

    elif len(sys.argv) == 5:
        x = sys.argv[1]
        x = x.replace(' ','') + "songs"
        try:
            n = int(sys.argv[2])
            y = int(sys.argv[3])
        except:
            sys.exit("Wrong Parameters entered")
        output_name = sys.argv[4]
    else:
        sys.exit("Wrong number of parameters entered (Enter 4)")
        

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(x))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    vid_num = 0
    i = 0
    while i < n:
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[vid_num])
        print(yt.length)
        print("Downloading File "+str(i+1)+" .......")
        try:
            mp4files = yt.streams.filter(only_audio=True).first().download(filename='tempaudio-'+str(i)+'.mp3')
        except:
            vid_num += 1
            continue
        i += 1
        vid_num += 1

    print("Files downloaded.")
    print("Getting the mashup ready.....")

    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[0:y*1000]
    for i in range(1,n):
        aud_file = str(os.getcwd()) + "/tempaudio-"+str(i)+".mp3"
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[0:y*1000],crossfade=1000)
  
    try:
        fin_sound.export(output_name, format="mp3")
        print("File downloaded successfuly. Stored as " + str(output_name))
    except:
        sys.exit("Error saving file. Try differrent file name")
        
    if delete_after_use:
        for i in range(n):
            os.remove("tempaudio-"+str(i)+".mp3")


if __name__ == '__main__':
	main()
