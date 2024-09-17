#! /usr/bin/python3
import argparse
import subprocess
import urllib.request


# Conducts a Nikto scan on the user-specified server
def vulnerability_check(web_server_url):
    print("Note: This may take a few minutes.\n")
    nikto_scan = subprocess.run(
        ["nikto", "-h", web_server_url, "-Display", "3", "-ask", "no"],
        stdout=subprocess.PIPE, text=True
    )
    print("Scan Complete\n\n")
    usable_nikto_scan_result = ""
    for text in nikto_scan.stdout:
        usable_nikto_scan_result += text
    print(usable_nikto_scan_result)
    print(
        "\n\nNOTE: "
        "The above results are potential vulnerabilities in your system and may be worth manually looking into.\n"
    )


# Executes the bash command "apache2 -v" and formats the response
def check_current_version(): 
    installed_apache_version = subprocess.run(["apache2", "-v"], stdout=subprocess.PIPE, text=True)
    formatted_installed_version = ""
    # Creating the formatted_installed_version string
    for character in installed_apache_version.stdout:
        formatted_installed_version += character
    formatted_installed_version = formatted_installed_version[:29]
    return formatted_installed_version


# pulls the current in-release version from the publisher's page and formats the response
def check_newest_version():
    pulling_newest_version = urllib.request.urlopen("https://httpd.apache.org/download.cgi")
    read_url = pulling_newest_version.read()
    split_url = read_url.split()
    line_counter = 0
    # creating the formatted_newest_version string
    for line in split_url:
        line_counter += 1
        if line_counter == 461:
            # changing encoding from bytes (b') to utf-8
            new_version = line.decode("utf-8")
            formatted_newest_version = f"Server version: A{new_version[8:13]}/{new_version[17:23]}"
            return formatted_newest_version


# compares the installed version to the current release version.
def version_comparison(installed_apache_version, newest_apache_version):
    if installed_apache_version != newest_apache_version:
        print("You do not have the current version of Apache!")
        return False
    else:
        print("You have the current version of Apache installed.")
        return True


# updates the current installed version to the current release version
def update_current_version():
    subprocess.run(["sudo", "cp", "/etc/apache2/apache2.conf", "/etc/apache2/apache2-backup.conf"])
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    print("Updating has completed")
    

# applying patches to the Apache server
def applying_patches(apache2_conf_file):
    subprocess.run(["sudo", "cp", "/etc/apache2/apache2.conf", "/etc/apache2/apache2-backup.conf"])
    config_patch_text = (
        "ServerTokens Prod\n"
        "ServerSignature Off\n\n<Directory /opt/apache2/apache2>\n"
        "Options -Indexes\n</Directory>\n\nFileETag None\n\nTraceEnable off\n\nTimeout 60"
    )
    with open(apache2_conf_file, "a+") as config_file:
        config_file.write(config_patch_text)
    print("Apache hardening patch has been Applied")


# restarting the Apache server
def restarting_apache_server():
    subprocess.run(["sudo", "systemctl", "restart", "apache2"], stdout=subprocess.PIPE, text=True)
    print("Apache has been reset.")


# main control function
if __name__ == "__main__":
    # Creating command line controls
    # creating the user options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--compare_version", dest="version_comp",
        help="Compair installed version to newest in-release version", action="store_true"
    )
    parser.add_argument(
        "-u", "-update_version", dest="update_version",
        help="Updates installed version to in-release version", action="store_true"
    )
    parser.add_argument(
        "-f", "--file_location", type=str, dest="conf_file", help="Enter the path to the config file"
    )
    parser.add_argument(
        "-s", "--scan", type=str, dest="ip_address", help="Enter the IP address of the server"
    )
    parser.add_argument(
        "-r", "--restart", dest="restart_server",
        help="Restart Apache once patch has been applied.", action="store_true"
    )
    parser.add_argument(
        "-p", "--patch", dest="patch_config",
        help="Run the patching function. Requires [-f] and [-r] to be defined", action="store_true"
    )
    # creating the variables for the program
    version_comp = parser.parse_args().version_comp
    update_version = parser.parse_args().update_version
    conf_file = parser.parse_args().conf_file
    ip_address = parser.parse_args().ip_address
    restart_server = parser.parse_args().restart_server
    patch_config = parser.parse_args().patch_config
    args = parser.parse_args()
    # making "help" the default when no flags are given
    if not version_comp and not update_version and not conf_file and not ip_address and not restart_server and not patch_config:
        print("Use -h for more info on using this program")
        exit(0)

# running the main program
    if args.version_comp:
        version_comparison(check_current_version(), check_newest_version())
        print()
    if args.update_version:
        update_current_version()
        print()
    if args.ip_address:
        vulnerability_check(ip_address)
        print()
    if args.patch_config and args.conf_file:
        applying_patches(conf_file)
    if args.patch_config and not args.conf_file:
        print("You must specify the location of the config file [-f]")
    if args.restart_server:
        restarting_apache_server()
