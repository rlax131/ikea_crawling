#!/usr/bin/env python
# coding: utf-8

# In[9]:


from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import urllib.request
import os
import sys

url = "https://www.ikea.com/kr/ko/cat/bookcases-10382/"
driver = webdriver.Chrome()

driver.get(url)
time.sleep(1)

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    time.sleep(2)

    try:
        btn_more = driver.find_element(By.XPATH, '//*[@id="product-list"]/div[3]/a/span')
        driver.execute_script("arguments[0].click();", btn_more)   # click() 대신 JS 클릭 안정적
        time.sleep(2)
    except:
        print(f"{i+1} 번째 반복에서 더보기 버튼 없음 → 루프 종료")
        break

html_code = driver.page_source
soup = bs(html_code,'html.parser')

root = soup.select_one('#product-list > div.plp-product-list__products.plp-product-list__products--compare-enabled')

names = root.select('div > div > div.plp-mastercard__price-components > a > div > div.plp-price-module__information > h3 > span.plp-price-module__name-decorator.notranslate > span')
sizes = root.select('div > div > div.plp-mastercard__price-components > a > div > div.plp-price-module__information > h3 > span.plp-text.plp-typography-label-m.plp-typography-regular.plp-price-module__description')
prices = root.select('div > div > div.plp-mastercard__price-components > a > div > div.plp-price-module__price > div > div > span > span.notranslate > span > span.plp-price__integer')
thumbnails = root.select('div > div > div.plp-product__image__container > a > img.image.plp-product__image.plp-product__image--alt')

print("=== Name ===")
for name in names:
    print(name.get_text())

print()

print("=== Size ===")
for size in sizes:
    print(size.get_text())

print()

print("=== Price ===")
for price in prices:
    print(price.get_text())

print()

print("===Thumbnails===")
for thumbnail in thumbnails:
    print(thumbnail.get('src'))

