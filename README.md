# Monitoring webpages with Python and BeautifulSoup


I recently found myself looking for a new bike for my wife and a Canyon bicycle (not sponsored) was the ultimate choice. Even under normal circumstances, it can be quite challenging to purchase one, as demand appears to vastly exceed supply. Not wanting to rely on their alert emails, I decided to create a python script, which monitors the webpage for any changes and immediately alerts me via sms and/or email. Of course, if you use any modern browser you'll likely find an extension that does exactly that. However, the free versions are often limited, and to my knowledge do not include SMS functionality.
<br>

## General Strategy
1. Read the webpage URL and get the HTML data
2. Find the desired element on the page to monitor
3. If there are any changes compared to the previous entry, notify me; otherwise, wait a predetermined amount of time and repeat steps 1 and 2
