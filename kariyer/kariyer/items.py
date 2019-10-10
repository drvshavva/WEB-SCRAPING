# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KariyerItem(scrapy.Item):
    # define the fields for your item here like:
    ilan_baslik = scrapy.Field()
    sirket_adi = scrapy.Field()
    label = scrapy.Field()
    tecrube = scrapy.Field()
    egitim = scrapy.Field()
    genel_nit_is_tanimi = scrapy.Field()
    #yabanci_dil = scrapy.Field()
    sektor = scrapy.Field()
    departman = scrapy.Field()
    calisma_sekli = scrapy.Field()
    sehir = scrapy.Field()
    pass
