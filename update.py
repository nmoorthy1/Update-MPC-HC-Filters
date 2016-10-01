import urllib.request
import os
import sys
from bs4 import BeautifulSoup
import requests
import re
import time
import zipfile
import datetime
from datetime import timedelta

def checkYesterday(str):
	if "Yesterday" in str:
		yesterday = datetime.datetime.now() - timedelta(1)
		daynum = yesterday.strftime("%d")
		num = int(daynum[len(daynum) - 1])

		fullnum = int(daynum)

		if(fullnum < 11 or fullnum > 20):
			if num == 0 or num >= 4:
				daynum = daynum + "th"
			if num == 1:
				daynum = daynum + "st"
			if num == 2:
				daynum = daynum + "nd"
			if num == 3:
				daynum = daynum + "rd"
		else:
			daynum = daynum + "th"
		date = daynum+" "+yesterday.strftime("%B %Y")

		str = str.replace("Yesterday", date)
		# str = str + "\n"
		# print(str)
	return str

def main():
	madvr = "http://forum.doom9.org/showpost.php?p=1271414&postcount=1"
	madvrdl = "http://madshi.net/madVR.zip"

	lav = "http://forum.doom9.org/showpost.php?s=5aee4a0315e1bc9bba9346295f8308aa&p=1425963&postcount=1"
	lavdl = ""

	new = 0
	try:
		f = open(os.path.join(sys.path[0], "filter_versions"), "r+")
	except FileNotFoundError:
		f = open(os.path.join(sys.path[0], "filter_versions"), "w+")
		new = 1

	line = f.readline()
	madvr_ver = line[0:]
	madvr_ver = madvr_ver.rstrip()
	get_date = checkYesterday("Yesterday")
	response = requests.get(madvr)
	data = response.text
	soup = BeautifulSoup(data, "html.parser")
	find = soup.body.find_all(text=re.compile(madvr_ver))
	if(len(find) == 1 or get_date in madvr_ver):
		print("No new madVR version")
	if(len(find) == 0 or os.stat(f.fileno()).st_size == 0):
		print("Found new madVR version, downloading...")
		find = soup.body.find_all(text=re.compile('Last edited by madshi'))
		find = find[0]
		find = find.replace('\r','')
		find = find.replace('\n', '')
		find = find.replace('\t', '')
		# find = "Last edited by madshi; Yesterday at "
		find = checkYesterday(find)
		f.seek(0)
		f.write(find)
		# f.truncate()
		
		try:
			hdr = {'User-Agent': 'Mozilla/5.0'}
			req = urllib.request.Request(madvrdl, headers=hdr)
			response = urllib.request.urlopen(req)
			temp = madvrdl.rpartition('/')[2]
			out = open("./"+temp, "wb")
			out.write(response.read())
			out.close()
			fh = open(temp, 'rb')
			z = zipfile.ZipFile(fh)
			for name in z.namelist():
				z.extract(name,"./madVR/")
			fh.close()
			os.remove("madVR.zip")
		except urllib.error.HTTPError as err:
				if err.code == 403:
					print(err.code)
				else:
					raise

	next_line = f.tell()

	line = f.readline()
	lav_ver = line[0:]
	lav_ver = lav_ver.rstrip()

	response = requests.get(lav)
	data = response.text
	soup = BeautifulSoup(data, "html.parser")
	find = soup.body.find_all(text=re.compile(lav_ver))
	# print(find)
	if(len(find) == 1):
		print("No new LAV Filters version")
	if(len(find) == 0 or line == ""):
		print("Found new LAV Filters version, downloading...")
		find = soup.body.find_all(text=re.compile('released '))
		# print(find)
		find = find[0]
		find = find[1:]
		f.seek(next_line)
		f.write("\n"+find)
		f.truncate()

		try:
			hdr = {'User-Agent': 'Mozilla/5.0'}
			for link in soup.find_all('a', href=re.compile('^https://files.1f0.de/lavf/')):
				# print(link.get('href'))
				if ".exe" in link.get('href'):
					lavdl = link.get('href')
					break
			lavdl = lavdl.rstrip()
			req = urllib.request.Request(lavdl, headers=hdr)
			response = urllib.request.urlopen(req)
			temp = lavdl.rpartition('/')[2]
			out = open("./"+temp, "wb")
			out.write(response.read())
			out.close()
			os.system(temp)
		except urllib.error.HTTPError as err:
				if err.code == 403:
					print(err.code)
				else:
					raise

	f.close()

main()