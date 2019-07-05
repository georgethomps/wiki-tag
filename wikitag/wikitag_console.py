"""Console application to quickly tag albums"""
from twisted.internet.error import ReactorNotRestartable

from albumtagger.album_tagger import AlbumTagger


def main():
    paths = []
    urls = []

    # TODO: warn user that files must be in order and that the tags will be changed in-place
    print('Welcome to the WikiTag console application!\n')
    print("WARNING: Each albums' music files must be alphabetically sorted in the order of the track list!\n")

    while True:
        directory = input('Drag your album folder here and press enter: ')
        scrape_link = input('Enter the Wikipedia link for your album and press enter: ')

        paths.append(directory)
        urls.append(scrape_link)

        print('Album queued for tagging\n')

        while True:
            proceed = None
            try:
                proceed = input('Would you like to add another album? (y/n): ').lower()[0]
            except IndexError:  # user presses enter with no input
                continue

            if proceed in {'y', 'n'}:
                break
            else:
                print('Invalid answer!\n')

        if proceed != 'y':
            break
        else:
            print()

    tagger = AlbumTagger(album_paths=paths,
                         album_urls=urls)
    tagger.tag_albums()  # Note that this will also end up printing untagged files/folders

    print('Thanks for using the WikiTag console application!')


if __name__ == '__main__':
    main()
