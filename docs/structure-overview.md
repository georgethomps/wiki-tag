# Project Structure Overview

What follows is an overview of the entire project's structure as well as an explanation for each module's role
in the context of the entire project:

**Legend**

CAPS TITLE: `Project Folder`
Standard Case: `Python Module`

&nbsp;

**Project Structure**

WIKITAG: `source code`

&nbsp;&nbsp; ALBUMSCRAPER: `Source code for the AlbumScraper (used to scrape music data)`
&nbsp;

&nbsp;&nbsp;&nbsp; DATAMANAGEMENT: `Code used extract information from the scraped HTML data`
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; __init__.py
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; data_extractors.py: `Higher level code of the xpath's used to parse HTML data`
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; track_cleaner.py: `TrackCleaner class to handle minor details with HTML track data`
&nbsp;

&nbsp;&nbsp;&nbsp; SCRAPYMODULES: `Scrapy code used to facilitate the scraping process`
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; album.py: `Scrapy item used to store the scraped data of an album`
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; album_pipeline.py: `Scrapy pipeline used to send data to the AlbumScraper`
&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp; albums_spider.py: `Scrapy spider to crawl url's and handle parsing`
&nbsp;

&nbsp;&nbsp;&nbsp; __init__.py
&nbsp;

&nbsp;&nbsp;&nbsp; album_scraper.py: `Code for the AlbumScraper class`
&nbsp;

&nbsp; ALBUMTAGGER: `Source code for the AlbumTagger (used to scrape music data and tag files)`
&nbsp;

&nbsp; __init__.py
&nbsp;

&nbsp; wikitag_console.py: `Console application that I designed for friends to use`


&nbsp;&nbsp;















































