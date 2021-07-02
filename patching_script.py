#! /usr/bin/python3
import sys, subprocess, urllib.request
from scapy.all import * 

#code parts remaining:
#optional: use argparse to get config file locations and IP addresses and such


###SSH into a machine
def ssh_initiation():
    print("SSH is still a work in progress")

###conducts a Nikto scan on the user-specified server
def vulnerability_check(web_server_url):
    #print("This section checks the Apache web server for vulnerabilities.\n")
    print("Note: This may take a few minutes.")
    nikto_scan=subprocess.run(["nikto","-h",web_server_url,"-Display","3","-ask","no"],stdout=subprocess.PIPE,text=True)
    print("Scan Complete")
    useable_nikto_scan_result=""
    for text in nikto_scan.stdout:
        useable_nikto_scan_result+=text
    print(useable_nikto_scan_result)
    return useable_nikto_scan_result


###executes the bash command "apache2 -v" and formats the response
def check_current_version(): 
    installed_apache_version=subprocess.run(["apache2", "-v"],stdout=subprocess.PIPE,text=True)
    formatted_installed_version=""
    ###creating the formatted_installed_version string
    for character in installed_apache_version.stdout:
        formatted_installed_version+=character
    formatted_installed_version=formatted_installed_version[:29]
    return formatted_installed_version


###pulls the current in-release version from the publisher's page and formats the response
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
    backup_conf=subprocess.run(["sudo", "cp", "/etc/apache2/apache2.conf", "/etc/apache2/apache2-backup.conf"])
    #create_update_repository=subprocess.run(["sudo","add-apt-repository","ppa:ondreja/apache2"])
    update_repository=subprocess.run(["sudo","apt-get","update"])
    upgrading_serices=subprocess.run(["sudo","apt-get","upgrade"])
    print("Updating has completed")
    return backup_conf

###applying patches to the Apache server
def applying_patches(apache2_conf_file,restart_prompt):
    backup_conf=subprocess.run(["sudo","cp","/etc/apache2/apache2.conf", "/etc/apache2/apache2-backup.conf"])
    config_patch_text="ServerTokens Prod\nServerSignature Off\n\n<Directory /opt/apache2/apache2>\nOptions -Indexes\n</Directory>\n\nFileETag None\n\nTraceEnable off\n\nTimeout 60"
    with open(sys.argv[1],"a+") as config_file:
        config_file.write(config_patch_text)
    print("Patch Applied")
    if restart_prompt.lower()=="yes" or restart_prompt.lower()=="y":
        restart_apache=subprocess.run(["sudo","systemctl","restart","apache2"],stdout=subprocess.PIPE,text=True)
        print("Apache has been reset.")


###main control function
if __name__=="__main__":
    update_choice=input("Would you like to update to the current release version of Apache? (Y/n) ")
    vuln_check_option=input("Would you like to check for Vulnerabilities? (Y/n) ")
    if vuln_check_option.lower()=="yes" or vuln_check_option.lower()=="y":
        web_server_url=input("What is the IP of the webserver you are trying to scan? ") 
    patch_option=input("Would you like to apply the optional patches? (Y/n) ")
    if patch_option.lower()=="yes" or patch_option.lower()=="y":
        restart_prompt=input("Apache will need to be restarted for changes to take effect.\nRestart when completed? (Y/n) ")
    print()
    if version_comparison(check_current_version(), check_newest_version())==False:
        if update_choice.lower()=="yes" or update_choice.lower()=="y":
            update_current_version()
        print()
    if vuln_check_option.lower()=="yes" or vuln_check_option.lower()=="y":
        vulnerability_check(web_server_url)
        print()
    if patch_option.lower()=="yes" or patch_option.lower()=="y":
        applying_patches(sys.argv[1],restart_prompt)
