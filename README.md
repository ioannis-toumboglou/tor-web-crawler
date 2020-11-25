# Tor Network Web Crawler
<br>
<b>NOTE: This application was developed and presented for my Master's degree thesis.</b>
<br>
<br>
The application initially creates a list of <b>Tor network</b> URLs, stores them in an <b>SQL</b> database, while
checking their status, whether they are active or not. Then the HTML content from these webpages is retrieved and stored in the database.
<br>
<br>
Three retrieval options are given to the user:<br>
<br>
<b>1. Random crawl</b>
<br>
   The user gives an initial url (seed) and a number of pages.
   The crawler creates a list of all the links found in first page and then chooses
   randomly which page to crawl next. This continues until the number of pages
   is reached.
<br>  
<br>
<b>2. Serial crawl</b>
<br>
   The user gives an initial url (seed) and next page format (eg. =page2).
   The crawler searches for next pages until no more pages are found.
   This function is ideal when crawiling eg. forums and only a specific post needs
   to be collected.
<br>
<br>
<b>3. Breadth-first crawl</b>
<br>
   The user gives an initial url (seed) and the desired level to be reached.
   For every page, the crawler gets all of the links found and stores their content in
   the database. Then repeats the same procedure for each one of them, thus implementing
   a breadth-first search.
<br>   
While collecting the content, the text found in these pages is extracted and stored seperately.
<br>
<br>
Finally, an unsupervised machine learing algorithm is used in order to classify it, based on the cyber-threat type it refers to.

The machine learning algorithm used is <b>K-Means</b>.

The database is implemented with <b>SQLite</b>.
