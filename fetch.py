#!/usr/bin/env python3

from os import system
from time import sleep
import re, urllib.request, sys

done = False
while not done:
	sys.stdout.write("Leave blank to exit.\n1: Wallhaven - Random\n2: Wallhaven - Search\n3: 4channel\n4: Cyberdrop\n5: Tenor - GIFs\n6: Danbooru - Search\n")

	try:
		selection = int(input(">>> "))
		if not selection:
			done = True

		match selection:
		# Random from Wallhaven
			case 1:
				try:
					url = "https://wallhaven.cc/search?categories=111&purity=110&atleast=1920x1080&sorting=random&order=desc"
					req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
					html = urllib.request.urlopen(req)
				except Exception as e:
					print(f"Nope. {e}")
					done = True
					break

				# Collect and convert thumbnail id to full image links (data-wallpaper-id="abc123" -> w.wallhaven.cc/full/ab/wallhaven-abc123.jpg)
				dictFromResult = dict.fromkeys(re.findall("data-wallpaper-id=\"([a-zA-Z0-9]{3,10})\"", html.read().decode()))
				listOfId = list(dictFromResult)

				for ID in listOfId:
					image = f"https://w.wallhaven.cc/full/{ID[0:2]}/wallhaven-{ID}.jpg"
					system(f"wget -q {image} -P ~/Downloads/Random/")
					print(f"Downloading {listOfId.index(ID) + 1} of {len(listOfId)} to ~/Downloads/Random/", end="\r")
				done = True
				print(f"\n{len(listOfId)} images saved.")

		# Search Wallhaven
			case 2:
				search = "+".join(input("Search: ").split(" "))
				try:
					url = f"https://wallhaven.cc/search?q={search}&categories=111&purity=110&sorting=random"
					req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
					html = urllib.request.urlopen(req)
				except Exception as e:
					print(f"Nope. {e}")

				# Collect and convert thumbnail id to full image links (data-wallpaper-id="abc123" -> w.wallhaven.cc/full/ab/wallhaven-abc123.jpg)
				dictFromResult = dict.fromkeys(re.findall("data-wallpaper-id=\"([a-zA-Z0-9]{3,10})\"", html.read().decode()))
				listOfId = list(dictFromResult)

				for ID in listOfId:
					image = f"https://w.wallhaven.cc/full/{ID[0:2]}/wallhaven-{ID}.jpg"
					system(f"wget -q {image} -P ~/Downloads/Search/")
					print(f"Downloading {listOfId.index(ID) + 1} of {len(listOfId)} to ~/Downloads/Search/", end="\r")
				done = True
				print(f"\n{len(listOfId)} images saved.")

		# 4chan
			case 3:
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
				dictFromResult = dict.fromkeys(re.findall("(i\.4cdn\.org\/[a-z]{1,4}\/[0-9]{1,20}\.[a-z]{2,4})", html.read().decode()))
				listOfFiles = list(dictFromResult)
				threadNumber = re.findall("thread/([0-9]{2,22}).", url)[0]

				for file in listOfFiles:
					# Download to folder named with thread number.
					system(f"wget -q https://{file} -P ~/Downloads/{threadNumber}/")
					print(f"Downloading {file.split('/')[-1]} to ~/Downloads/{threadNumber}/", end="\r")
				done = True
				print(f"\n{len(listOfFiles)} files saved.")

		# Cyberdrop
			case 4:
				albumId = input("Enter album ID (the last alphanumerical part of the URL)\n>>> ")

				try:
					url = f"https://cyberdrop.me/a/{albumId}"
					req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
					html = urllib.request.urlopen(req)
				except Exception as e:
					print(f"Nope. {e}")
					done = True
					break

				dictFromResult = dict.fromkeys(re.findall("data-src=\"(.{10,})\" data-type", html.read().decode()))
				listOfFiles = list(dictFromResult)

				for file in listOfFiles:
					system(f"wget -q {file} -P ~/Downloads/{albumId}")
					print(f"Downloading {listOfFiles.index(file) + 1} of {len(listOfFiles)} to ~/Downloads/{albumId}/", end="\r")
				done = True
				print(f"\n{len(listOfFiles)} files saved.")

		# TENOR
			case 5:
				search = input("Enter search term(s).\n>>> ")
				number = input("How many gifs would you like?\nPlease enter a number between 1-50. Any higher may potentially break the process.\n>>> ")
				try:
					url = f"https://www.tenor.com/search/{'-'.join(search.split(' '))}-gifs"
					req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
					html = urllib.request.urlopen(req)
				except Exception as e:
					print(f"Nope. {e}")
					done = True
					break

				dictFromResult = dict.fromkeys(re.findall("(https://c.tenor.com/[a-zA-Z0-9]{2,}/[a-zA-Z0-9\-]{3,}.gif)", html.read().decode()))
				listOfFiles = list(dictFromResult)[0:int(number)]

				for file in listOfFiles:
					system(f"wget -q {file} -P ~/Downloads/gifs/")
					print(f"Downloading {listOfFiles.index(file) + 1} of {len(listOfFiles)} to ~/Downloads/gifs/", end="\r")
				done = True
				print(f"\n{len(listOfFiles)} files saved.")

		# danbooru
			case 6:
				search = input("Search: ")
				try:
					url = f"https://danbooru.donmai.us/posts?tags={'_'.join(search.split(' '))}"
					req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
					html = urllib.request.urlopen(req)
				except Exception as e:
					print(f"Nope. {e}")

				dictFromResult = dict.fromkeys(re.findall("src=\".{10,}\/([a-zA-Z0-9]{1,3}\/[a-zA-Z0-9]{1,3}\/.{10,}\.[a-zA-Z0-9]{3,4})\"", html.read().decode()))
				listOfId = list(dictFromResult)

				print(listOfId)

				for ID in listOfId:
					image = f"https://cdn.donmai.us/original/{ID}"
					print(image)
					system(f"wget -q {image} -P ~/Downloads/Search/")
					print(f"Downloading {listOfId.index(ID) + 1} of {len(listOfId)} to ~/Downloads/Search/", end="\r")
				done = True
				print(f"\n{len(listOfId)} images saved.")

	except Exception:
		print("\nEnter an option as listed.")

