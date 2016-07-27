import urllib.request
import os
import sys
from bs4 import BeautifulSoup
import requests
import re
import time
import zipfile

madvr = "http://forum.doom9.org/showpost.php?p=1271414&postcount=1"
madvrdl = "http://madshi.net/madVR.zip"

lav = "http://forum.doom9.org/showpost.php?s=5aee4a0315e1bc9bba9346295f8308aa&p=1425963&postcount=1"
lavdl = ""
f = open(os.path.join(sys.path[0], "madvrver"), "r+")


line = f.readline()
madvr_ver = line[8:]
madvr_ver = madvr_ver.rstrip()
response = requests.get(madvr)
data = response.text
soup = BeautifulSoup(data, "html.parser")
find = soup.body.find_all(text=re.compile(madvr_ver))
if(len(find) == 1):
	print("No new madVR version")
if(len(find) == 0):
	print("Found new madVR version, downloading...")
	find = soup.body.find_all(text=re.compile('Last edited by madshi'))
	find = find[0]
	find = find.replace('\r','')
	find = find.replace('\n', '')
	find = find.replace('\t', '')
	f.seek(0)
	f.write("madVR - ")
	f.write(find)
	f.truncate()
	
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
f.close()

f = open(os.path.join(sys.path[0], "lavver"), "r+")
line = f.readline()
lav_ver = line[6:]
lav_ver = lav_ver.rstrip()
# print(lav_ver)

response = requests.get(lav)
data = response.text
soup = BeautifulSoup(data, "html.parser")
find = soup.body.find_all(text=re.compile(lav_ver))
# print(find)
if(len(find) == 1):
	print("No new LAV Filters version")
if(len(find) == 0):
	print("Found new LAV Filters version, downloading...")
	find = soup.body.find_all(text=re.compile('released '))
	# print(find)
	find = find[0]
	find = find[1:]
	f.seek(0)
	f.write("LAV - ")
	f.write(find)
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