##########################################
##                                      ##
##          LINKS LIST CREATOR          ##
##              FUNCTIONS               ##
##                                      ##
##########################################




from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import random
from time import sleep
import socks
import socket
from stem import Signal
from stem.control import Controller
from fake_useragent import UserAgent
import sys

import crawler_backend



## Get actual url (http or https)
def get_url(url):
    if url.startswith('https'):
        url = url[8:]
    if url.startswith('http'):
        url = url[7:]
    page_inserted = requests.get('http://' + url)
    url = page_inserted.url
    
    return url



## Links retrieval
def get_links(url):
    res = requests.get(url)
    c = res.content
    soup = BeautifulSoup(c, 'html.parser')

    # Get all types of links and add them in a set
    hrefs = list()
    for link in [h.get('href') for h in soup.find_all('a')]:
        hrefs.append(link)

    for link in hrefs:
        if link is None:
            hrefs.remove(link)

    hrefs = set(hrefs)

    links = list()

    for link in hrefs:
        if '.onion' in link:
            index = link.index('.onion')
            new_url = link[index-16:index] + '.onion'
            links.append(new_url)

    unique_links = set(links)
    links = list(unique_links)
    
    return links



## Next link retrieval
def get_next_links(url, next_page_style, number_of_pages):
    next_links = list()
    
    for i in range(2, number_of_pages+1):
        next_links.append(url + next_page_style + str(i))

    return next_links



## Get rid of security id if existent in url
def no_sid(url):
    if 'sid=' in url:
        pos = url.index('sid=')
        next_pos = pos+37
        url = url[:pos]+url[next_pos:]
    elif 's=' in url:
        pos = url.index('s=')
        next_pos = pos+37
        url = url[:pos]+url[next_pos:]

    if url.endswith('&'):
        url = url[:-1]
    elif url.endswith('?'):
        url = url[:-1]

    return url



## Change url
def change_url(url):
    links_list = get_links(url)
    index = random.randint(0, len(links_list)-1)
    next_url = links_list[index]
    url = next_url
    url = get_url(url)

    return url



## Find the next url, if there is one
def find_new_url(url):
    page_found_counter = 0
    while True:
        url = change_url(url)
        found = crawler_backend.check_url(url)
        if not found:
            page_found_counter = 0
            url = get_url(url) 
            return url 
        else:
            print('Searching for a new page to crawl... (%s)\n' %url)
            page_found_counter += 1
            if page_found_counter == 30:
                print('\nThere are no more pages to collect')
                sys.exit()
            else:
                continue



## Check url for errors
def check_error_status(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return True
    except requests.exceptions.RequestException as err:
        print()
        print (err)
        print()
        return False
    except requests.exceptions.HTTPError as errh:
        print()
        print (errh)
        print()
        return False
    except requests.exceptions.ConnectionError as errc:
        print()
        print (errc)
        print()
        return False
    except requests.exceptions.Timeout:
        print()
        print (errt)
        print()
        return False



# Connect to the Tor network
def open_tor_connection():
    #Set a default proxy, which all further socksocket objects will use
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9150)
    #Return a socket object, which is assigned to socket.socket and which opens a socket
    socket.socket = socks.socksocket
    # Perform DNS resolution through the socket
    socket.getaddrinfo = getaddrinfo



# Perform DNS resolution through the socket
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]



# Change IP Address and User Agent
def set_new_ip():
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
    sleep(controller.get_newnym_wait())

    ua.random



controller = Controller.from_port(port=9151)
ua = UserAgent()
open_tor_connection()


# Random crawling
def crawl(url):
    url = get_url(url)
    links = get_links(url)

    for link in links:
        try:
            link = get_url(link)
            found = crawler_backend.check_url(link)
            if found:
                print('\n' + link + ' is already in the database.')
                print('Skipped...')
                continue
            else:
                print('\nInserting... ' + link)
                crawler_backend.insert_page(link)
                crawler_backend.insert_status(link, 'Alive')
                print('Status : Alive')
                
        except:
            print('\nInserting... ' + link)
            link = 'http://' + link
            crawler_backend.insert_page(link)
            crawler_backend.insert_status(link, 'Offline')
            print('Status : Offline')
            pass
        
# Serial crawling
def serial_crawl(url, next_page_style, number_of_pages):
    url = get_url(url)
    print('\nCreating list..')
    # Create next pages links
    next_links = get_next_links(url, next_page_style, number_of_pages)
    # Create the whole links list
    links_list = list()
    links_list.append(url)
    links_list = links_list + next_links
    print('\nList created..')

    print('\nCrawling links..')
    for link in links_list:
        link = get_url(link)
        crawl(link)
