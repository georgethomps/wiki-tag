# wiki-tag

**Project Summary**

Wiki-tag is a webscraping framework built off of Scrapy that is designed to scrape music data from Wikipedia.
The heart of the framework resides in the AlbumScraper class, which functions similarly to a Scrapy Spider.
Additionally, users can use the AlbumTagger class to scrape music data and tag music files with such data.

&nbsp

**Important Project Guidelines

The following is a list of a guidelines that should be read before working with wiki-tag:

1. An AlbumScraper can only be run once (this is due to the nature of the Scrapy and Twisted frameworks)
2. Only one instance of an AlbumScraper should be implemented in one's code
3. The filenames for an album's tracks must be alphabetically sorted by track number (most music files are)
4. Some audio formats may not work; these will be implemented in future updates through the tag_map module

&nbsp

**Framework Weaknesses**

Currently, wiki-tag is still in the process of development. The framework will work well with most albums
out there, but the following exceptions will need to be amended in future updates:

1. Older albums in which the track list is broken up by Vinyl sides
2. Deluxe Edition tracks (the standard edition tracks work)
3. Classical albums (maybe, this genre is a nightmare to tag and not very popular)

Aside from these scraping weaknesses, there are a few other general framework issues:

1. The framework was designed to work with FLAC; other audio formats may not work (URGENT)

&nbsp

**Moving Forward**

As of now, I've nearly reached a year ever since I started learning Python. I've never been more proud of
a project than wiki-tag and I intend to stick with it to improve the functionality and intelligibility of
the code. If anyone would like to contribute or offer advice, feel free to email me at ghthompson19@gmail.com

I hope you all enjoy wiki-tag!




























































