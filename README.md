# RoboFinder
Fetch and parse all robots.txt from "web.archive" and extracting URL and Sitemap

## Requirements
Python3.6+
pip3 install -r requirements.txt

## How to use?

## Options:
-h, --help                show this help message and exit
-u URL, --url=URL         Enter your target url
-d DELAY, --delay=DELAY
      Enter amount of delay between each request
      Default: 0.5(s)
-a, --address   Show robots.txt paths
-s, --sitemap   Show robots.txt sitemaps

## Examples
[+] Showing all paths from memoryleaks.ir
python robofinder.py -u https://memoryleaks.ir -a
[+] Showing all sitemaps from memoryleaks.ir
python robofinder.py -u https://memoryleaks.ir -s
[+] Showing both Paths and Sitemaps of memoryleaks.ir
python robofinder.py -u https://memoryleaks.ir -a -s
[+] Delay 3s between each web.archive request
python robofinder.py -u https://memoryleaks.ir -a -d 3
