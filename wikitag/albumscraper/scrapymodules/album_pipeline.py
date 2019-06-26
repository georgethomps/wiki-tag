class AlbumPipeline(object):

    @staticmethod
    def process_item(item, spider):
        """Utilizes the call by sharing parameter passing method to retrieve and store the scraped data.
        The item will be stored in the passed spider's memory, which ends up being passed to the out scraping
        class's memory (the spider's memory references the scraper's memory)."""
        spider.memory_link.append(item)
        return item
