#!/usr/bin/env python3

from os import system
from time import sleep
import re, urllib.request, sys

# Set user agent for some shitty sites

done = False
while not done:
	sys.stdout.write("1: Random Wallpapers\n2: Search\n3: 4channel URL\n4. Cyberdrop Album")
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

	# Search Wallhaven
	elif selection == 2:
		search = input("Search: ")
		try:
			url = f"https://wallhaven.cc/search?q={search}&categories=111&purity=110&sorting=random"
			req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}")
			
		# Collect and convert thumbnail id to full image links (data-wallpaper-id="abc123" -> w.wallhaven.cc/full/ab/wallhaven-abc123.jpg)
		dictFromResult = dict.fromkeys(re.findall(r'data-wallpaper-id="([a-zA-Z0-9]{3,10})"', html.read().decode()))
		listOfId = list(dictFromResult)
		
		for ID in listOfId:
			image = f"https://w.wallhaven.cc/full/{ID[0:2]}/wallhaven-{ID}.jpg"
			system(f"wget -q {image} -P ~/Downloads/Random/")
			print(f"Downloading {listOfId.index(ID) + 1} of {len(listOfId)} to ~/Downloads/Search/", end="\r")
		done = True
		print(f"\n{len(listOfId)} images saved.")

	# 4chan
	elif selection == 3:
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

	# Cyberdrop
	elif selection == 4:
		albumId = input("Enter album ID (the last alphanumerical part of the URL)\n>>> ")
		
		try:
			url = f"https://cyberdrop.me/a/{albumId}"
			req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}")
			done = True
			break
			
		dictFromResult = dict.fromkeys(re.findall(r'data-src="(.{10,})" data-type', html.read().decode()))
		listOfFiles = list(dictFromResult)
		
		for file in listOfFiles:
			system(f"wget -q {file} -P ~/Downloads/{albumId}")
			print(f"Downloading {listOfId.index(file)} of len(listOfFiles) to ~/Downloads/{albumId}", end="\r")
		done = True
		print("\n{len(listOfFiles) files saved.}")
