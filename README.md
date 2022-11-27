# Untrusted-Scraper

This was supposed to be my mona lisa, but I realized after creating my scraping that it was simply not a good idea. 
Maybe another fan of this game will use this, or someone who wants to learn about scraping will analyze my very bad code. However, this is done.


# Features
From a single Opsec link, it will create a folder containing:

Username, Profile link, img link, Color, and Consumable in users.csv

The entire div for the topology. Half assed way to get it, but it works. Needs jQuery. In topology.csv

Username and Message for prechat, in prechat.csv

Color, Starting role, Finishing role, and Dead/alive in opsummary.csv

And finally, the bane of my existence: messages.csv
Identifies what time a message was sent (ie. Prep Night or Day 3), What is a action, what is a event, and whether a message was sent in ASC, dead chat, or alive chat. Also includes indicators for broadcasts, mail, votes. All of that and the html code of the message.

 # How To Use

This is simple enough, but here it is:

1. Download and extract the code.
2. Download all the python packages. I would use ``` pip install -r requirements.txt ```.
3. Open both the scraper.py and messages2.py file in any text editor, and replace the URL on line 9 and 8 respectively with the opsec you are wishing to scrape.
4. Run scraper.py. Once it is completed, run messages2.py

And that should be it!
