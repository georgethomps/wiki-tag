"""Console application to quickly tag albums"""
from albumtagger.album_tagger import AlbumTagger


def main():
    print('Welcome to the WikiTag console application!\n')

    while True:
        directory = input('Drag your album folder here and press enter: ')
        scrape_link = input('Enter the Wikipedia link for your album and press enter: ')

        tagger = AlbumTagger(album_path=directory,
                             album_url=scrape_link)
        tagger.tag_tracks()  # Note that this will also end up printing untagged files/folders

        proceed = None
        while True:
            proceed = input('Would you like to tag another album? (y/n): ').lower()[0]

            if proceed in {'y', 'n'}:
                break
            else:
                print('Invalid answer!')

        if proceed != 'y':
            break

    print('Thanks for using the WikiTag console application!')
