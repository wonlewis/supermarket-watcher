import scrapy
from varname import nameof
from datetime import datetime
import time

drinks = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=drinks&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=drinks&sorting=POPULARITY&storeId=165&url=drinks'
vegetables = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=fruits-vegetables&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=fruits-vegetables&sorting=POPULARITY&storeId=17&url=fruits-vegetables'
dairy = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=dairy-chilled-eggs&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=dairy-chilled-eggs&sorting=POPULARITY&storeId=17&url=dairy-chilled-eggs'
bakery = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=bakery&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=bakery&storeId=17&url=bakery'
meat = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=meat-seafood&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=meat-seafood&sorting=POPULARITY&storeId=17&url=meat-seafood'
staples = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=rice-noodles-cooking-ingredients&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page={}&pageType=category&slug=rice-noodles-cooking-ingredients&sorting=POPULARITY&storeId=17&url=rice-noodles-cooking-ingredients'
household = 'https://website-api.omni.fairprice.com.sg/api/product/v2?category=household&experiments=promolabel-a%2CsearchVariant-B%2CtimerVariant-Z%2CinlineBanner-A%2CsubstitutionBSVariant-A%2Cgv-A%2Cshelflife-B%2CcSwitch-A%2Cds-A%2Csimpleprice-b%2Cpromocopy-a%2Calgolia-b%2Cls_comsl-B%2Csearchrec-off%2Cls_deltime-A%2Cls_sscart-A&includeTagDetails=true&orderType=DELIVERY&page=2&pageType=category&slug=household&sorting=POPULARITY&storeId=17&url=household'
my_list = [drinks, vegetables, dairy, bakery, meat, staples, household]
my_list_name = ['drinks', 'vegetables', 'dairy', 'bakery', 'meat', 'staples', 'household']

class QuotesSpider(scrapy.Spider):
    name = "scrap_fp"
    url = drinks.format(1)

    def start_requests(self):
        utc_time = datetime.utcnow()
        crawl_ts = int(time.time())
        yield scrapy.Request(
            url=self.url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            },
            callback=self.parse,
            meta={
                'crawl_ts': crawl_ts,
                'utc_time': utc_time,
                'this_element': 0
            }
        )

    def parse(self, response):
        #read json object
        my_data = response.json()
        utc_time = response.meta['utc_time']
        crawl_ts = response.meta['crawl_ts']
        this_element = response.meta['this_element']

        for product in my_data["data"]["product"]:
            if 'offers' in product:
                offer_price = product["offers"][0]["price"]
                offer_description = product["offers"][0]["description"]
            else:
                offer_price = None
                offer_description = None
            print(dir())
            yield {
                'barcode': product["barcodes"][0],
                'brand': product["brand"]["name"],
                'id': product["brand"]["id"],
                'name': product["name"],
                'slug': product["slug"],
                'images': product["images"],
                'mrp': product["storeSpecificData"][0]["mrp"],
                'updated_at': product["storeSpecificData"][0]["updatedAt"],
                'offer_price': offer_price,
                'offer_description': offer_description,
                'display_unit': product["metaData"]["DisplayUnit"],
                "SAP_product_name": product["metaData"]["SAP Product Name"],
                'product_type': my_list_name[this_element],
                'utc_time': utc_time,
                'crawl_ts': crawl_ts

            }
        curr_page = my_data["data"]["pagination"]["page"]
        total_page = my_data["data"]["pagination"]["total_pages"]
        if curr_page < 2:
            next_page_url = my_list[this_element].format(curr_page+1)
            yield scrapy.Request(
                url=next_page_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                },
                callback=self.parse,
                meta={
                    'crawl_ts': crawl_ts,
                    'utc_time': utc_time,
                    'this_element': this_element
                }
                )
        elif this_element < len(my_list) - 1:
            this_element += 1 
            next_page_url = my_list[this_element].format(1)
            print("NEXT PAGE:", this_element, next_page_url)
            yield scrapy.Request(
                url=next_page_url, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                },
                callback=self.parse,
                meta={
                    'crawl_ts': crawl_ts,
                    'utc_time': utc_time,
                    'this_element': this_element
                })

