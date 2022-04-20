#!/usr/bin/env python3

from os import system
from time import sleep
import re, urllib.request, sys

done = False
while not done:
	sys.stdout.write("1: Random wallpapers\n2: 4channel URL\n")
	selection = int(input(">>> "))
	
	# Random from Wallhaven
	if selection == 1:
		try:
			url = "https://wallhaven.cc/search?categories=111&purity=110&atleast=1920x1080&sorting=random&order=desc"
			req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}")
			done = True
			break
		
		# Collect and convert thumbnail id to full image links (data-wallpaper-id="abc123" -> w.wallhaven.cc/full/ab/wallhaven-abc123.jpg)
		dictFromResult = dict.fromkeys(re.findall(r'data-wallpaper-id="([a-zA-Z0-9]{3,10})"', html.read().decode()))
		listOfId = list(dictFromResult)
		
		for ID in listOfId:
			image = f"https://w.wallhaven.cc/full/{ID[0:2]}/wallhaven-{ID}.jpg"
			system(f"wget -q {image} -P ~/Downloads/Random/")
			print(f"Downloading {listOfId.index(ID) + 1} of {len(listOfId)} to ~/Downloads/Random/", end="\r")
		done = True
		print(f"\n{len(listOfId)} images saved.")
				
	# 4chan
	elif selection == 2:
		url = input("Paste full thread URL here\n>>> ")
		# fetch thread page
		try:
			req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}, please enter the full URL\nie. boards.4channel.org/xyz/thread/1234567")
			done = True
			break
		
		# Get list of file (png, jpg, webm, gif, whatever) links from "href" in HTML (without "s")
		dictFromResult = dict.fromkeys(re.findall(r"(i\.4cdn\.org\/[a-z]{1,4}\/[0-9]{1,20}\.[a-z]{2,4})", html.read().decode()))
		listOfFiles = list(dictFromResult)
		threadNumber = re.findall("thread/([0-9]{2,22}).", url)[0]
		
		for file in listOfFiles:
			# Download to folder named with thread number.
			system(f"wget -q https://{file} -P ~/Downloads/{threadNumber}/")
			print(f"Downloading {file.split('/')[-1]} to ~/Downloads/{threadNumber}/", end="\r")
		done = True
		print(f"\n{len(listOfFiles)} files saved.")
