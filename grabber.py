#!/usr/bin/python3

import requests
from sys import argv

locale = "fr"
url = "https://www.google.%s" %locale
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"
user_agent = "Mozilla/5.0 (X11; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0"
headers = {'User-Agent': user_agent,
           'Cookie':'NID=76=Dgfp32-g4nDlRRXGDFldcXxOb2fdabmC8wo-mdgMG-T7-18KUiX5M20eukLEy_oP9vhFbzqtXuruf5ITaUW-XS9xszBsNvfDwmG4O8ZJIoNxO-Gc2AwRwpQ9Pw1da6n9cnqK4_MN-ABnn_Nzto96nSRm8nCGJC-yOjQqHitds0zu0rK_ob33fplDOsZGM1xRLbXctVv7TR6UpWCzdWRuA7HrCHitfkLH_w; SID=DQAAACoBAADXpGQgEJaimUYRUPBy0VpAw_b0HDZlevCA0Pr4-PL729_t1Al4LncyVnW4-Dvi-F4ofWH6Er2M3E6_8a7fXcHuYzeZa3ty9q6FmWkYeXDxHvxxX0kXAPSxlvlxBCkLwFs8Hiisq36Sv6N8RShTallxIdbvETDUJRpTB30klGw0-5D_35jEvrrLKER5wFiJdulcX5XWppRVe7TOHYSYUB3al4T23UKreMy5ZYD0Xe9f-VDk04PX_hfHKBZr-MXO-2_Pp3BXr-H7h7mUYRzCkfLbg3jQRpzo0lzJtEu9ReS9sH8J80IzxBNoVXGlyJu53B5V-dHQL0ckEIFbrJsHh3n6rHv2L19kuhjzsGNGqjPRNM9Yl8F4dnlnbt-jv5ysalIYj4bS-8vKOYm4rLdNHwSf; HSID=AajWrq_rXRqs5HoVe; SSID=AH3_7DH47_PMlprW7; APISID=cmYQyL0RMF2UyrE6/AIttYazRM-9tpva3a; SAPISID=_8e4u3abX_mQcpv-/AMJfioxYkl0KhQPpu; OGPC=5061821-17:; DV=wmhayRsL4D0gSqReJQiheV5K6gJapUobuFqWO-2ATQAAAAA'
}

additional_params="aqs=chrome.0.69i59j69i65l3j69i57j69i61.420j0j7&sourceid=chrome&es_sm=0&ie=UTF-8&sclient=psy-ab"

def usage():
    print('usage : %s "query"' %argv[0])
    return 1

def get_links_from_text(text):
    links = []
    splits = text.replace("https://", "http://").split("http://")
    for split in splits:
        if not "google" in split:
            find = split.find('"')
            if split.find('<') < find:
                find = split.find('<')
            if len(split[:find]) > 0:
                links.append(split[:find])
    return links

def get_links(query, page):
    get_request = url+"/search?q=%s&oq=%s&start=%s&%s" %(query.replace(" ", "+"), query.replace(" ", "+"), page*10, additional_params)
    print("Query : [%s]" %get_request)
    r = requests.get(get_request, headers=headers)
    if (r.status_code == 200):
        return get_links_from_text(r.text)
    print(r.text)
    return []

def main():
    if len(argv) != 2:
        return usage()
    else:
        print(get_links(argv[1], 0))
    return 0

if __name__ == "__main__":
    main()
