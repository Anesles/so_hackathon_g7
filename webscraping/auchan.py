import requests
import re
from bs4 import BeautifulSoup
import datetime

def	get_auchan(ean):

	url = "https://www.auchan.pt/pt/pesquisa?q=" + str(ean)
	response = requests.get(url)
	soup = BeautifulSoup(response.content, "html.parser")
	StoreName = "Auchan"

	try:
		product_link = soup.find_all('a', class_='auc-product-tile__image-container__image')[0]['href']
	except:
		raise Exception("Auchan: Product not found.")
	
	product_link = "https://www.auchan.pt" + product_link
	response = requests.get(product_link)
	soup = BeautifulSoup(response.content, "html.parser")

	try:
		price = soup.find_all('span', class_='value')[0].text
		price = price.replace(',', '.')
		price = re.sub(r'[^0-9.]+', '', price)
		price = float(price)
	except:
		raise Exception("Auchan: Price not found.")

	try:
		capacity = soup.find_all('li', class_="attribute-values auc-pdp-regular")[0].text
		capacity = re.sub(r'[^0-9.]+', '', capacity)
		capacity = float(capacity) * 1000
		capacity = int(capacity)
	except:
		capacity = "N/A"

	try:
		discount = soup.find_all('div', class_='auc-promo--discount--red')[0].text
		discount = 1
	except:
		discount = 0

	img = soup.find_all('img', class_='d-block img-fluid auc-carousel__image')[0]['src']

	return[ean, StoreName, 0, price, discount, "€", datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))), "Portugal", product_link]