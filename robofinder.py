import requests
from optparse import OptionParser
import sys
import time
import re
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


parser = OptionParser()

parser.add_option("-u", "--url", dest="url", help="Enter your target url",
                  default=False)

parser.add_option("-d", "--delay", dest="delay", help="Enter amount of delay between each request\n\tDefault: 0.5(s)",
                  default=0.5)

parser.add_option("-a", "--address", dest="address", help="Show robots.txt paths",
                  default=False, action="store_true")

parser.add_option("-s", "--sitemap", dest="sitemap", help="Show robots.txt sitemaps",
                  default=False, action="store_true")

parser.add_option("-q", "--quite", dest="quite", help="Silent output messages.",
                  default=False, action="store_true")

parser.add_option("-v", "--verbose", dest="verbose", help="Show debug level messages.",
                  default=False, action="store_true")

(options, args) = parser.parse_args()

if not options.url:
    print("Please enter URL in following format: scheme://domain.tld")
    sys.exit(0)

if "http" not in options.url.lower():
    print("Please enter URL with it's scheme. (http|https)")
    sys.exit(0)

if options.url.count("/") > 3:
    print("Please only enter domain name, not full URL\nFormat: scheme://domain.tld")
    sys.exit(0)

try:
    int(options.delay)
except:
    print("Please enter a valid value for delay.")
    sys.exit(0)

if not options.address and not options.sitemap:
    print("[!] Please either use -a or -s in order to extract data.")
    sys.exit(0)


def print_message(message):
    if not options.quite:
        print(message)


def print_verbose(message):
    if options.verbose:
        print(message)


base_domain = options.url
if base_domain[-1] == "/":
    base_domain = base_domain[:-1]
domain = f"{base_domain}/robots.txt"


list_of_timestamps_url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json&filter=statuscode:200&fl=timestamp,original&collapse=digest"
response = requests.get(list_of_timestamps_url, verify=False, timeout=15).json()
list_of_timestamps = []

for item in response:
    if item[0] != "timestamp":
        try:
            timestamp = item[0]
            address = item[1]
        except Exception as e:
            print_verbose(f"[debug] Error On Request: {e}")
            continue
        request_address = f"http://web.archive.org/web/{timestamp}if_/{address}"
        # request_address = f"http://web.archive.org/web/{timestamp}/{address}"
        list_of_timestamps.append(request_address)

print_message(f"[+] Found [{len(list_of_timestamps)}] Timestamps.")

address_regex = "(?i)allow(\s?)\:(\s?)(.*)"
sitemap_regex = "(?i)(sitemap|site-map)(\s?)\:(\s?)(.*)"
target_sitemaps = set()
target_urls = set()

print_message("[+] Fetching timestamps...")
for timestamp in list_of_timestamps:
    print_verbose(f"[debug] Getting New Timestamp Data.\n\t{timestamp}")
    time.sleep(int(options.delay))
    try:
        response = requests.get(timestamp, verify=False, timeout=15).content.decode("utf-8")
    except Exception as e:
        print_verbose(f"[debug] Error On Request: {e}")
        continue
    for line in response.split("\n"):
        address_matched_items = re.findall(address_regex, line)
        sitemap_matched_items = re.findall(sitemap_regex, line)

        if len(address_matched_items) > 0:
            try:
                matched_address = address_matched_items[0][-1]
                if "/" not in matched_address[0]:
                    matched_address = f"/{matched_address}"
            except:
                continue

            final_url = f"{base_domain}{matched_address}"
            if options.address and final_url not in target_urls:
                print(final_url)
            target_urls.add(final_url)

        if len(sitemap_matched_items) > 0:
            try:
                final_sitemap = sitemap_matched_items[0][-1]
                if options.sitemap and final_sitemap not in target_sitemaps:
                    print(final_sitemap)
                target_sitemaps.add(final_sitemap)
            except:
                continue

if options.address and not options.quite:
    if len(target_urls) < 1:
        print("No URL found from robots.txt")

if options.sitemap and not options.quite:
    if len(target_sitemaps) < 1:
        print("No sitemap found from robots.txt")
