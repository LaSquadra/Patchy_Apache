#! /usr/bin/python3
import sys, subprocess, urllib.request
from scapy.all import * 

#code parts remaining:
#optional: use argparse to get config file locations and IP addresses and such
#check the Apache web server for vulnerabilities
#update to the current verison 
#AND/OR
#explore further patching options


###SSH into a machine
def ssh_initiation():
    print("SSH is still a work in progress")

###conducts a Nikto scan on the user-specified server
def vulnerability_check():
    print("This section checks the Apache web server for vulnerabilities. \n")
    web_server_url=input("What is the IP of the webserver you are trying to scan? ")
    print("Note: This may take a few minutes.")
    nikto_scan=subprocess.run(["nikto" , "-h", web_server_url, "-Display", "3", "-ask", "no"], stdout=subprocess.PIPE, text=True)
    print("Scan Complete")
    useable_nikto_scan_result=""
    for text in nikto_scan.stdout:
        useable_nikto_scan_result+=text
    print(useable_nikto_scan_result)
    return useable_nikto_scan_result


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
    backup_conf=subprocess.run(["sudo", "cp", "etc/apache2/apache2.conf", "/etc/apache2/apache2-backup.conf"])
    create_update_repository=subprocess.run(["sudo","apt-add-repository","ppa:ondreja/apache2"])
    update_repository=subprocess.run(["sudo","apt-get","update"])
    upgrading_distribution=subprocess.run(["sudo","apt-get","dist-upgrade"])
    print("Updating has completed")

###applying patches to the Apache server
def applying_patches():

    print("The patching section is still under development.")


###main control function
if __name__=="__main__":
    #print(check_current_version().strip())
    #print(check_newest_version().strip())
    if version_comparison(check_current_version(), check_newest_version())==False:
        update_choice=input("Would you like to update to the current release version of Apache? (Y/n) ")
        if update_choice.lower()=="yes" or update_choice.lower()=="y":
            update_current_version()
        else: 
            print("Alternate patching options are currently under development")
    vulnerability_check()
