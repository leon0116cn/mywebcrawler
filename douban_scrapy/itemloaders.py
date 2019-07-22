from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Identity


class DoubanMovieTop250ItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    movie_name_out = Join(separator='')
    image_urls_out = Identity()

