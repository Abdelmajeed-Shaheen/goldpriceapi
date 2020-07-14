from woocommerce import API
from random import randrange
import json
import requests
import pprint


wcapi = API(
    url="https://abdelmajeedshaheen.com/",
    consumer_key="ck_d4bcd7cde4803c56c2571da72185a33e5c062162",
    consumer_secret="cs_5e61014458a2dbca53825b77fccecf78b1355c48",
    wp_api=True,
    version="wc/v3",
    query_string_auth=True
)

r =requests.get('https://metals-api.com/api/latest?access_key=sv2xjdgvxss49ah7qfg3hcciz53jks3p76ka0cfks56em139fpp3pagqbs9z&base=KWD&symbols=XAU')
metals_data = r.json()
price_per_ounce = metals_data['rates']['XAU']
price_per_gram = round((price_per_ounce / 31.103),2)

page = 1
while True:
  products = wcapi.get('products', params={'per_page': 100, 'page': page}).json()
  for pro in products:
      product_weight = int(pro['weight'])
      manufacturing_price = 0
      for d in pro['meta_data']:
        if d['key'] == 'manufacturing_price':
            manufacturing_price = int(d['value'])
      product_price =(price_per_gram + manufacturing_price + 0.2)*product_weight
      product_price = round(product_price,1)
      url = "products/"+str(pro['id'])
      data = {
         "regular_price": str(product_price)
         }
      wcapi.put(url, data)
      print("//")
  if len(products) == 0: 
    break
  page = page + 1
print('finished')
#other api access key 
# ac3eee41537b4c9d6feb4e3349652cadac3eee41