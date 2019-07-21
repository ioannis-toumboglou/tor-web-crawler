from bs4 import BeautifulSoup

import crawler_backend
import tor_crawler_functions as function


## Text categorization
def text_classification(text):
    text = text.lower()
    category = "Undefined"

    for word in ["malware" , "virus" , "ransomware" , "worm" , "spyware" , "adware" , "trojan" , "rootkit" , "backdoor"]:
        if word in text and text.count(word)>2:
            category = "Malware"
    for word in ["phishing" , "whaling" , "deceptive phishing" , "spear phishing" , "pharming"]:
        if word in text and text.count(word)>2:
            category = "Phishing"
    for word in ["mitm" , "man in the middle" , "man in middle" , "m-i-t-m" , "man-in-the-middle" , "ip spoofing" , "rogue access point" , "ssl hijack"  , "ssl hijacking" , "arp spoof" , "arp spoofing" , "dns spoof" , "dns spoofing"]:
        if word in text and text.count(word)>2:
            category = "Man in the Middle"
    for word in ["dos" , "ddos" , "denial of service" , "denial-of-service", "distributed denial" , "bot" , "botnet"]:
        if word in text and text.count(word)>2:
            category = "DoS"
    for word in ["sql injection" , "sql" , "database", "sql-injection"]:
        if word in text and text.count(word)>2:
            category = "SQL Injection"
    for word in ["zeroday" , "zero day" , "0day", "zero-day", "zero"]:
        if word in text and text.count(word)>2:
            category = "Zero Day"
    for word in ["xss" , "cross site" , "cross site scripting" , "site scripting", "cross-site-scripting", "cross-site"]:
        if word in text and text.count(word)>2:
            category = "XSS"

    return category


records = crawler_backend.page_content()

for record in records:
    url = record[1]
    category = record[2]
    html_code = record[3]
    text = record[4]

    if category == None:
        category = text_classification(text)
        crawler_backend.insert_category(url, category)

print('Text classification completed!')
