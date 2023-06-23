import scrapy

from pymongo import MongoClient 

from pathlib import Path


client = MongoClient("mongodb+srv://test1:test12345678@cluster0.7nr31nz.mongodb.net/")

db=client.flipkart

def insert_data(page , title , price , ratings):
    collections=db[page]
    data={
         'title':title,
         'price':price,
         'ratings':ratings
    }

    post_id = collections.insert_one(data).inserted_id
    return post_id


class PagedataSpider(scrapy.Spider):
    name = "pagedata"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://flipkart.com"]

    def start_requests(self):
        urls = [
            "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&param=7564&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlNob3AgTm93Il0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D&otracker=clp_metro_expandable_2_7.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q1PDG4YW86MF_wp4&fm=neo%2Fmerchandising&iid=M_94018fb3-2424-4157-a0ad-7205e5d4e039_7.Q1PDG4YW86MF&ppt=hp&ppn=homepage&ssid=cqwouudpa80000001687544539639",
            "https://www.flipkart.com/televisions/pr?sid=ckf%2Cczl&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&otracker=categorytree&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.brand%255B%255D%3DLG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG&otracker=nmenu_sub_TVs%20%26%20Appliances_0_LG"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"pagedata-{page}.html"
         
         #For storing data as a FILE

        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")



        p_title=response.css('._4rR01T::text').getall()
        print(p_title)
        p_prices = response.css('._30jeq3._1_WHN1::text').getall()
        print(p_prices)
        p_ratings=response.css('._2_R_DZ span span:nth-of-type(1)::text').getall()
        print(p_ratings)

        

        #for inserting data in mongoDB

        for title , price , rating in zip(p_title , p_prices , p_ratings):
            res=insert_data(page , title , price , rating)

            print("inserting data into a database.....")
        else:
            print("Data has been inserted  to the database successfully....")
           
            

