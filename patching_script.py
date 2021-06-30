#! /usr/bin/python3
import sys, subprocess, urllib.request
from scapy.all import * 

#Psudo code for now?
#use argparse to get config file locations and IP addresses and such
#check the host machine for current version of Apache
#check the Apache for vulnerabilities
#check for the current version of Apache: https://httpd.apache.org/download.cgi
def check_current_version():
    installed_apache_version=subprocess.run(["apache2", "-v"])
    return installed_apache_version

def check_newest_version():
    newest_apache_version=urllib.request.urlopen("https://httpd.apache.org/download.cgi")
    print("Result code: " + str(newest_apache_version.getcode()))
    return newest_apache_version

def version_comparison():    
    if installed_apache_version!=newest_apache_version:
        print(installed_apache_version)
        print("You do not have the current version of Apache!")
    else:
        print("You have the current verion of Apache installed.")



if __name__=="__main__":
    check_current_version()
    check_newest_version()
    #version_comparison()
                           
