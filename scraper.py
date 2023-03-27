user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
headers = {'User-Agent': user_agent}
from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['products']
collection = db['scraper']

url = 'https://fr.aliexpress.com/category/205000231/Laptops.html?category_redirect=1&spm=a2g0o.productlist.104.10.4c6e2f5bL6AMdX'
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.content, 'html.parser')

products = soup.find_all('div', class_='manhattan--content--1KpBbUi')

data = []
for product in products:
    name = product.find('h1', class_='manhattan--titleText--WccSjUS').text.strip()
    price = product.find('div', class_='manhattan--price-sale--1CCSZfK').text.strip()
    data = {'name': name, 'price': price}
    collection.insert_one(data)

