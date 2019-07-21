##########################################
##                                      ##
##          LINKS LIST CREATOR          ##
##           MAIN APPLICATION           ##
##                                      ##
##########################################



from time import sleep
import os
import socket

import crawler_backend
import tor_links_list_creator_functions as function


# Check to see if there is a database in progress...
check = crawler_backend.view_urls()

if len(check) != 0:
    print('\nAn active data collection progress is found\n')
    print('OPTIONS')
    print('- Press 1 to create a new file and start a fresh crawl')
    print('- Any key to continue current collection')
    choice = input('\nUser input: ')
    if choice == '1':
        os.remove('crawler_database.db')
        print('\nRemoving file...\n')
        sleep(1)
        print('File removed!\n')
        crawler_backend.connect()
    else:
        print()
        

while True:
    # Get the initial page from the user
    print('OPTIONS')
    print('1 - Crawl a page')
    print('2 - Serial Crawl')
    print('3 - Quit')
    
    choice = input('\nUser input: ')
    
    if len(choice) < 1:
        print("\nYou haven't typed anything!\n")
        continue
    
    if (choice == '1'):
        url = input('\nEnter a URL: ')
        url = function.get_url(url)
        if function.check_error_status(url):
            pass
        else:
            continue
        crawler_backend.connect()
        print('\nProcessing...\n')
        sleep(1)
        function.crawl(url)
        print('Done!\n')
        answer = input('Continue? (y/n) ')
        print()
        answer.lower()
        if answer == 'y':
            continue
        else:
            pass
        
    elif (choice == '2'):
        url = input('\nEnter a URL: ')
        url = function.get_url(url)
        next_page_style = input('\nEnter the next page style (eg. page=2): ')
        number_of_pages = int(input('\nEnter the number of pages: '))
        if function.check_error_status(url):
            pass
        else:
            continue
        crawler_backend.connect()
        print('\nProcessing...\n')
        sleep(1)
        function.serial_crawl(url, next_page_style, number_of_pages)
        print('Done!\n')
        answer = input('Continue? (y/n) ')
        print()
        answer.lower()
        if answer == 'y':
            continue
        else:
            pass
      
    elif (choice == '3'):
        print('\nHave a nice day!\n')
        break
    
    else:
        print('This is not a valid selection!\n')
        continue
    
    break
