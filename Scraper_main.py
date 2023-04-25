# Scraper_main.py
# Scrape pages and iteratively save to file

import pandas as pd
from Product_scraper import lxml_scraper # user function
import requests
import time

def check_existing_file(csv_path, all_links):
    '''
    Input: csv_path of active file, master link list

    Output:
    1. If DF doesn't exist at c   sv_path, create one
    2. If DF does exist, remove duplicates in all_links to continue scraping
    '''

    try: 
        df = pd.read_csv(csv_path,index_col= None)
    except: 
        df = pd.DataFrame(columns=[
            'link', 'title', 'error_page', 'detail_paragraph', 'detail_items',
            'size_fit_desc', 'categories', 'color', 'color_price'])
        df.to_csv(csv_path, index = False)

    used_links = df.link.to_list()
    all_links = [i for i in all_links if i not in used_links]

    return all_links


def main():

    # open link doc ------------------------------------------------------
    input_path = '/Users/cristinconnerney/Desktop/Instalily/data/links.txt'
    csv_path = '/Users/cristinconnerney/Desktop/Instalily/data/product1.csv'

    all_links = []
    with open(input_path,'r') as infile:
        for line in infile:
            all_links.append(line.strip('\n'))

    # Testing: -----------------------------------------------------------

    # all_links = all_links[:100]

    # Check existing outfile ---------------------------------------------

    all_links = check_existing_file(csv_path, all_links)

    # Scraper -------------------------------------------------------------

    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})

    for n, product_page in enumerate(all_links):
        print(n)

        page = lxml_scraper(headers, product_page)

        table_df = pd.DataFrame([page])
        table_df.to_csv(csv_path, header=False, index=False, mode='a')

if __name__ == '__main__':
    main()
