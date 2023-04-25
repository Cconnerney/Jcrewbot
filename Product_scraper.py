# Product_scraper.py
# Scrape data from a product page

import requests
from bs4 import BeautifulSoup
import numpy as np

from bs4 import SoupStrainer as strainer
from lxml import etree


def lxml_scraper(headers, link):
    '''
    Input: product page link
    Function: scrape product page for all desired fields
    Output: dictionary with product page information
    '''

    res = requests.get(link, headers=headers)

    soup = BeautifulSoup(res.content, 'html.parser')
    dom = etree.HTML(str(soup))

    try: 
        if 'Thank you for your patience' or 'Let’s try this again' in dom.xpath("/html/body/div/div/div/h1")[0].text:
            error = True
        else:
            error = np.nan
    except: 
        error = np.nan

    try: 
        title = dom.xpath("//*[@id='product-name__p']")[0].text
    except: 
        title = np.nan

    try: 
        detail_paragraph = dom.xpath("//*[@id='product-description']/p")[0].text
    except: 
        detail_paragraph = ''

    try: 
        detail_items = dom.xpath("//*[@id='product-description']/ul/li")
        detail_items = [item.text for item in detail_items]
    except: 
        detail_items = np.nan

    try: 
        size_fit_desc = dom.xpath('//*[@id="product-size-fit"]/ul/li')
        size_fit_desc = [item.text for item in size_fit_desc]
    except: 
        size_fit_desc = np.nan

    try: 
        categories = dom.xpath('//*[@id="page__p"]/div/div/ul/li/a/h3')
        categories = [item.text for item in categories]
    except: 
        categories = np.nan

    try: 
        color = soup.findAll('div',{'class':'ProductPriceColors__color___xobW5'})
        color = [i['data-name'] for i in color]
        color_price = [i['aria-label'] for i in color]
    except: 
        color = np.nan
        color_price = np.nan


    product_data = {
        'link': link,
        'title': title,
        'error_page': error,
        'detail_paragraph': detail_paragraph,
        'detail_items': detail_items,
        'size_fit_desc': size_fit_desc,
        'categories': categories,
        'color': color,
        'color_price': color_price
    }

    return product_data

