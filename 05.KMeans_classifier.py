from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import string

import crawler_backend


## Search for keywords in text, remove punctuation
def keywords_in_text(keywords, text):
    for c in string.punctuation:
        text = text.replace(c," ")
    
    return set(keywords).intersection(text.split())

def KMeansClassifier(text):
    ## Cyber attacks are divided in eight categories
    ## Marketplaces is a point of interest
    
    ## Data collected per category from files
    malware = open('Cyber Threats/malware.txt', 'r').read()
    phishing = open('Cyber Threats/phishing.txt', 'r').read()
    MITM = open('Cyber Threats/MITM.txt', 'r').read()
    DoS = open('Cyber Threats/DoS.txt', 'r').read()
    SQL_injection = open('Cyber Threats/SQL_injection.txt', 'r').read()
    zero_day = open('Cyber Threats/zero_day.txt', 'r').read()
    XSS = open('Cyber Threats/XSS.txt', 'r').read()
    credential_reuse = open('Cyber Threats/credential_reuse.txt', 'r').read()
    carding = open('Cyber Threats/carding.txt', 'r').read()
    marketplace = open('Cyber Threats/marketplace.txt', 'r').read()

    ## Unify all texts
    document = [malware, phishing, MITM, DoS, SQL_injection, zero_day, XSS, credential_reuse, carding, marketplace]

    ## TF-IDF on texts
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(document)

    ## Apply the K-Means algorithm on data
    true_k = 10
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, random_state=3425)
    model.fit(X)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    ## Show the clusters
    #for i in range(true_k):
    #    print("Cluster %d:" % i),
    #    for ind in order_centroids[i, :10]:
    #        print('%s' % terms[ind])
    #    print()

    # Create a list of the 15 most common words for each category
    marketplace = list()
    for ind in order_centroids[0, :15]:
        marketplace.append(terms[ind])

    MITM = list()
    for ind in order_centroids[1, :15]:
        MITM.append(terms[ind])

    malware = list()
    for ind in order_centroids[2, :15]:
        malware.append(terms[ind])

    SQL_injection = list()
    for ind in order_centroids[3, :15]:
        SQL_injection.append(terms[ind])
        
    carding = list()
    for ind in order_centroids[4, :15]:
        carding.append(terms[ind])
        
    credential_reuse = list()
    for ind in order_centroids[5, :15]:
        credential_reuse.append(terms[ind])

    zero_day = list()
    for ind in order_centroids[6, :15]:
        zero_day.append(terms[ind])

    XSS = list()
    for ind in order_centroids[7, :15]:
        XSS.append(terms[ind])

    phishing = list()
    for ind in order_centroids[8, :15]:
        phishing.append(terms[ind])

    DoS = list()
    for ind in order_centroids[9, :15]:
        DoS.append(terms[ind])

    text = text.lower()

    if len(keywords_in_text(malware, text))>2:
        return "Malware"
    elif len(keywords_in_text(phishing, text))>2:
        return "Phishing"
    elif len(keywords_in_text(MITM, text))>2:
        return "Man-in-the-middle"
    elif len(keywords_in_text(DoS, text))>2:
        return "DoS"
    elif len(keywords_in_text(SQL_injection, text))>2:
        return "SQL Injection"
    elif len(keywords_in_text(zero_day, text))>2:
        return "Zero Day"
    elif len(keywords_in_text(XSS, text))>2:
        return "XSS"
    elif len(keywords_in_text(credential_reuse, text))>2:
        return "Credential Reuse"
    elif len(keywords_in_text(carding, text))>2:
        return "Carding"
    elif len(keywords_in_text(marketplace, text))>2:
        return "Marketplace"
    else:
        return "Undefined"


records = crawler_backend.page_content()
count = 0

for record in records:
    url = record[1]
    threat_type = record[2]
    text = record[4]
    threat_type = KMeansClassifier(text)
    crawler_backend.insert_threat_type(url, threat_type)
    count += 1

print('Text classification completed!')
print('Number of records classified: ', count)
print()
