from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics+cards'

# opening up connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parser
page_soup = soup(page_html, "html.parser")

# grabs each product
containers = page_soup.findAll("div",{"class":"item-container"})

# creates csv file
filename = "products.csv"
f = open(filename, "w")

headers = "brand; product_name; prices; shipping\n"

f.write(headers)

# grabs the information of the product
for contain in containers:
    brand = contain.div.div.a.img["title"]

    title_container = contain.findAll("a", {"class":"item-title"})
    product_name = title_container[0].text

    shipping_container = contain.findAll("li", {"class":"price-ship"})
    shipping = shipping_container[0].text

    print("brand: " + brand)
    print("product_name: " + product_name)
    print("shipping: " + shipping)

    f.write(brand + ";" + product_name.replace(",", "|") + ";" + shipping + "\n")

f.close()
