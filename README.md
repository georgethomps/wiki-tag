# wiki-tag

**Project Summary**

Wiki-tag is a webscraping framework built off of Scrapy that is designed to scrape music data from Wikipedia.
The heart of the framework resides in the AlbumScraper class, which functions similarly to a Scrapy Spider.
Additionally, users can use the AlbumTagger class to scrape music data and tag music files with such data.

**Using the AlbumScraper**

Using the AlbumScraper is incredibly simple and functions similarly to a Scrapy Spider. You can manage the
albums you want to scrape by adding or removing album URL's through the "urls" attribute (it behaves like a list).
Once all of your url's are confirmed, you can scrape the music data with the "crawl" method (this can only be done
once).

Once your music data is scraped, you can access the data through the "albums" attribute. Each album is stored in
a TagMap, which is a dictionary of the metadata that can be used to tag music files (read the TagMap section for
more).

**List of TagMap Keys for Extracting Album-Level Data**
A TagMap (pending to be formally implemented) is the data structure used to store scraped album data. Here is a
list of the following keys that can be used to retrieve specific album data:

1. artist
2. album_artist: The same thing as artist (this probably should be removed)
3. album_title
4. year
5. genres: A tuple of genres found on the Wikipedia page (the first is used by default)
6. tracks: A list of named tuples which contain track-level information (read Track section for more)

**List of Track Keys for Extracking Track-Level Data**
A Track is a named tuple that stores track-level music data. Tracks contain the following keys:

1. No: Track number
2. Title
3. Writers: Same as the composer field for most tagging software
4. Producers: Common for Hip Hop albums, not common in most tagging software
5. Length

TODO: Add a section for the Album Tagger

**Important Project Guidelines**

The following is a list of a guidelines that should be read before working with wiki-tag:

1. An AlbumScraper can only be run once (this is due to the nature of the Scrapy and Twisted frameworks)
2. Only one instance of an AlbumScraper should be implemented in one's code
3. The filenames for an album's tracks must be alphabetically sorted by track number (most music files are)
4. Some audio formats may not work; these will be implemented in future updates through the tag_map module

**Framework Weaknesses**

Currently, wiki-tag is still in the process of development. The framework will work well with most albums
out there, but the following exceptions will need to be amended in future updates:

1. Older albums in which the track list is broken up by Vinyl sides
2. Deluxe Edition tracks (the standard edition tracks work)
3. Classical albums (maybe, this genre is a nightmare to tag and not very popular)

Aside from these scraping weaknesses, there are a few other general framework issues:

1. The framework was designed to work with FLAC; other audio formats may not work (URGENT)

**Moving Forward**

As of now, I've nearly reached a year ever since I started learning Python. I've never been more proud of
a project than wiki-tag and I intend to stick with it to improve the functionality and intelligibility of
the code. If anyone would like to contribute or offer advice, feel free to email me at ghthompson19@gmail.com

I hope you all enjoy wiki-tag!




























































