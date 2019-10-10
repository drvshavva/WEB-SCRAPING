# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep
from scrapy.selector import Selector
from ..items import KariyerItem
#bu programda kariyer.net sitesinden belirlenen kategori ismi belirtilerek arama yapilmasi ve sonuclarin bir csv dosyasina
#kaydedilmesi hedeflenmistir
#iletisim : drvshavva@gmail.com
class IlanlarSpider(scrapy.Spider):
    name = 'ilanlar'

    allowed_domains = ['www.kariyer.net']
    start_urls = ['https://www.kariyer.net/is-ilanlari']

    # olusturalacak kategori ismi
    sinif = 'banka-sigorta'
    #sonuclarin kaydedilmesi icin once gerekli dizini belirtiyoruz
    custom_settings = {'FEED_FORMAT': 'csv',
                       'FEED_URI': '/home/safir/kariyer/'+sinif +'_%(time)s.csv'}

    def parse(self, response):
        #bilgisayarinizda chromedriver'in oldugu dizini burada belirtiyoruz
        webdriver_path = '/home/safir/Desktop/chromedriver'
        self_driver = webdriver.Chrome(webdriver_path)
        self_driver.get('https://www.kariyer.net/is-ilanlari')

        #sayfada arama yapilan yere  kategori ismini yaziyoruz
        search_item = self_driver.find_element_by_xpath(' // *[ @ id = "txtSearchKeyword"]')
        search_item.clear()
        search_item.send_keys(IlanlarSpider.sinif)
        sleep(1.8)
        #kategori ismini yazdiktan sonra butona tikliyoruz
        next_page = self_driver.find_element_by_xpath('//*[@id="btnSearchKeyword"]')
        self_driver.execute_script("arguments[0].click();", next_page)
        sleep(4.5)

        items = KariyerItem()
        #next_page = 'https://www.kariyer.net/is-ilanlari'
        ilan_links = []
        page = 0
        #23 sayfadan ilanlara ait linkleri aliyoruz
        while page <= 23:
            scrapy_selector = Selector(text=self_driver.page_source)
            links = scrapy_selector.xpath('//a[@class="link position"]/@href').extract()
            for i in range(0, len(links)):
                ilan_links.append(links[i])

            #sonraki sayfaya geciyoruz
            next_page = self_driver.find_element_by_xpath('//a[@id="lnkNextPage"]')
            self_driver.execute_script("arguments[0].click();", next_page)
            page += 1
            sleep(4.8)

        #topladigimiz ilan linklerine gidip belirtilen ozellikleri aliyoruz
        for i in range(0, len(ilan_links)):
            url = 'https://www.kariyer.net' + ilan_links[i]
            self_driver.get(url)
            scrapy_selector = Selector(text=self_driver.page_source)
            genel = scrapy_selector.xpath("""//h3[contains(., 'GENEL NİTELİKLER VE İŞ TANIMI')]/following-sibling::node()//text()""").extract()
            if genel:
               items['ilan_baslik'] = scrapy_selector.xpath('//a[@id="jobTitle"]/text()').extract()
               items['sirket_adi'] = scrapy_selector.xpath('//a[@id="jobCompany"]/text()').extract()
               items['genel_nit_is_tanimi'] = genel
               #items['is_tanimi'] = scrapy_selector.xpath("""//div//h3[starts-with(., 'İŞ TANIMI')]/following-sibling::node()/descendant-or-self::text()""").extract()
               items['tecrube'] = scrapy_selector.xpath('//div[@class="sub-box aday-kriterleri"]/div[2]/div[1]/div[2]/p/text()').extract()
               items['egitim'] = scrapy_selector.xpath('//div[@class="sub-box aday-kriterleri"]/div[2]/div[3]/div[2]/p/text()').extract()
             # items['yabanci_dil'] = scrapy_selector.xpath('//div[@class="sub-box aday-kriterleri"]/div[2]/div[4]/div[2]/p/text()').extract()
               items['sektor'] = scrapy_selector.xpath('//div[@class="sub-box pozisyon-bilgileri"]/div[2]/div[1]/div[2]/p/text()').extract()
               items['departman'] = scrapy_selector.xpath('//div[@class="sub-box pozisyon-bilgileri"]/div[2]/div[2]/div[2]/p/text()').extract()
               items['calisma_sekli'] = scrapy_selector.xpath('//div[@class="sub-box pozisyon-bilgileri"]/div[2]/div[3]/div[2]/p/text()').extract()
               items['sehir'] = scrapy_selector.xpath('//div[@class="sub-box pozisyon-bilgileri"]/div[2]/div[6]/div[2]/p/text()').extract()
               items['label'] = IlanlarSpider.sinif
               sleep(5)

               yield items









