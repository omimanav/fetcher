from os import system
import re, urllib.request, sys

done = False
while not done:
	# Invalid input
	if len(sys.argv) > 3:
		print("Enter only the URL of the thread as the first parameter followed by destination directory ie:\n$ python3 4chMediaFetch.py https://website.com/pageWithImages.html ~/Downloads/images/\n")
		done = True
	else:
		try:
			req = urllib.request.Request(sys.argv[1], headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}")
			done = True
			break

		dictFromResult = dict.fromkeys(re.findall(r"src=(\"https\:\/\/www\.[a-z0-9A-Z]{2,}\.[a-z]{2,4}\/[a-z\-\_]{1,}\/[a-z0-9A-Z]\.[a-z]{2,4})\"", html.read().decode()))
		listOfImages = list(dictFromResult)

		for image in listOfImages:
			if len(sys.argv) == 3:
				system(f"wget -q https://{image} -P {sys.argv[2]}")
				print(f"Downloading {image} to {sys.argv[2]}...")
			else:
				system("wget -q https://{image} -P ~/Downloads/{sys.argv[1].split('/')[-1]}/")
				print(f"Downloading {image} to ~/Downloads/{threadNumber}/ folder...")
		done = True
		print(f"{len(listOfImages)} files saved.")
