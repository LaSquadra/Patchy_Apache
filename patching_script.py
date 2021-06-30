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
    return installed_apache_version.stdout

def check_newest_version():
    newest_apache_version=urllib.request.urlopen("https://httpd.apache.org/download.cgi")
    read_url=newest_apache_version.read()
    split_url=read_url.split()
    line_counter=0
    for line in split_url:
        line_counter+=1
        if line_counter==461:
            new_version=line.decode("utf-8")
        if line_counter==463:
            build_date=line.decode("utf-8")
            #print(line_counter,line)
    server_version=("Server version: A"+new_version[8:13]+"/"+new_version[17:23])
    server_build_date=("Server built:   "+build_date[:10])
    print(server_version + '\n' + server_build_date)
    #print("Result code: " + str(newest_apache_version.getcode()))
    #print(read_url)
    return newest_apache_version

def version_comparison():    
    if installed_apache_version!=newest_apache_version:
        print(installed_apache_version)
        print("You do not have the current version of Apache!")
        return False
    else:
        print("You have the current verion of Apache installed.")
        return True

def update_current_version():
    print("This section is still under development")


if __name__=="__main__":
    print(check_current_version().strip())
    check_newest_version()
    #if version_comparison()==False:
    #    update_current_version()
