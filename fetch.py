from os import system
from time import sleep
import re, urllib.request, sys

done = False
while not done:	
	# Invalid input
	if len(sys.argv) > 3:
		print("Enter only the URL of the thread as the first parameter followed by destination directory ie:\n$ python3 4chMediaFetch.py https://boards.4chan.org/ic/thread/0123456789 \"~/Downloads/images/\"")
	# Check website, currently only 4chan
	elif "boards.4chan" not in sys.argv[1]:
		print("Enter a 4chan/4channel thread URL only. I'm working on compatibility with other websites.")
		done = True
	else:
		try:
			req = urllib.request.Request(sys.argv[1], headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"})
			html = urllib.request.urlopen(req)
		except Exception as e:
			print(f"Nope. {e}")
			done = True
			break

		dictFromResult = dict.fromkeys(re.findall(r"(i\.4cdn\.org\/[a-z]{1,4}\/[0-9]{1,20}\.[a-z]{2,4})", html.read().decode()))
		listOfImages = list(dictFromResult)
		threadNumber = sys.argv[1].split("/")[-1].split("#")[0]
		for image in listOfImages:
			if len(sys.argv) == 3:
				# Download to foldedr with specified name.
				system(f"wget -q https://{image} -P {sys.argv[2]}")
				print(f"Downloading {image} to {sys.argv[2]}...", end="\r")
			else:
				# Download to folder named with thread number.
				system("wget -q https://{image} -P ~/Downloads/{sys.argv[1].split('#')[0].split('/')[-1]}/")
				print(f"Downloading {image} to ~/Downloads/{threadNumber}/...", end="\r")
		done = True
		print(f"{len(listOfImages)} files saved.", end="\r")
