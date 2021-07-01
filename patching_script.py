#! /usr/bin/python3
import sys, subprocess, urllib.request
from scapy.all import * 

#code parts remaining:
#optional: use argparse to get config file locations and IP addresses and such
#check the Apache web server for vulnerabilities
#update to the current verison 
#AND/OR
#explore further patching options


###executes the bash command "apache2 -v" and formats the response
def check_current_version(): 
    installed_apache_version=subprocess.run(["apache2", "-v"], stdout=subprocess.PIPE, text=True)
    formatted_installed_version=""
    ###creating the formatted_installed_version string
    for character in installed_apache_version.stdout:
        formatted_installed_version+=character
    formatted_installed_version=formatted_installed_version[:29]
    return formatted_installed_version


###pulls the current release version from the publisher's page and formats the response
def check_newest_version():
    pulling_newest_version=urllib.request.urlopen("https://httpd.apache.org/download.cgi")
    read_url=pulling_newest_version.read()
    split_url=read_url.split()
    line_counter=0
    ###creating the formatted_newest_version string
    for line in split_url:
        line_counter+=1
        if line_counter==461: 
            ###changing encoding from bytes (b') to utf-8
            new_version=line.decode("utf-8")
            formatted_newest_version=("Server version: A"+new_version[8:13]+"/"+new_version[17:23])
    return formatted_newest_version


###compares the installed version to the current release version.
def version_comparison(installed_apache_version,newest_apache_version): 
    if installed_apache_version!=newest_apache_version:
        print("You do not have the current version of Apache!")
        return False
    else:
        print("You have the current verion of Apache installed.")
        return True
###updates the current installed version to the current release version
def update_current_version():
    print("The updating section is still under development.")

###main control function
if __name__=="__main__":
    #print(check_current_version().strip())
    #print(check_newest_version().strip())
    if version_comparison(check_current_version(), check_newest_version())==False:
        update_choice=input("Would you like to update to the current release version of Apache? (Y/n) ")
        ###update_choice does not correctly evaluate the input <--still needs work.
        print(update_choice)
        if update_choice.lower()=="yes" or update_choice.lower()=="y":
            update_current_version()
        else: 
            print("Alternate patching options are currently under development")
