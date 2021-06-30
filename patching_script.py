#! /usr/bin/python3
import sys, subprocess, urllib.request
from scapy.all import * 

#Psudo code for now?
#use argparse to get config file locations and IP addresses and such
#check the host machine for current version of Apache
#check the Apache for vulnerabilities
#check for the current version of Apache: https://httpd.apache.org/download.cgi
def check_current_version():
    installed_apache_version=subprocess.run(["apache2", "-v"], stdout=subprocess.PIPE, text=True)
    formatted_installed_version=""
    for character in installed_apache_version.stdout:
        formatted_installed_version+=character
    formatted_installed_version=formatted_installed_version[:29]
    return formatted_installed_version

def check_newest_version():
    getting_newest_version=urllib.request.urlopen("https://httpd.apache.org/download.cgi")
    read_url=getting_newest_version.read()
    split_url=read_url.split()
    line_counter=0
    for line in split_url:
        line_counter+=1
        if line_counter==461:
            new_version=line.decode("utf-8")
    newest_server_version=("Server version: A"+new_version[8:13]+"/"+new_version[17:23])
    return newest_server_version

def version_comparison(installed_apache_version,newest_apache_version):    
    if installed_apache_version!=newest_apache_version:
        print("You do not have the current version of Apache!")
        return False
    else:
        print("You have the current verion of Apache installed.")
        return True

def update_current_version():
    print("This section is still under development")


if __name__=="__main__":
    #print(check_current_version().strip())
    #print(check_newest_version().strip())
    version_comparison(check_current_version(), check_newest_version())
    #if version_comparison()==False:
    #     update_current_version()
    #else:
    #    print("You are running the newest version of Apache.)
