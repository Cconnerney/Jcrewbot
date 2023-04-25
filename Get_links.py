# Get_links.py
# Save links for all PDP pages

import xmltodict
import requests
from bs4 import BeautifulSoup

def get_pdp_sitemaps(master):
    '''
    Input: master sitemap directory
    Output: array of PDP sitemap links
    '''

    res = requests.get(master)
    raw = xmltodict.parse(res.text)

    data = [r["loc"] for r in raw["sitemapindex"]["sitemap"]]
    data = [link for link in data if "pdp" in link]

    return data

def extract_links(xml_url):
    '''
    Input: PDP sitemap link
    Output: array of product page links 
    '''
    r = requests.get(xml_url)
    xml = r.text
    soup = BeautifulSoup(xml,features="lxml")

    links_arr = []
    for link in soup.findAll('loc'):
        linkstr = link.getText('', True)
        links_arr.append(linkstr +'\n')

    return links_arr 


def main():

    master = "https://www.jcrew.com/sitemap-wex/sitemap-index.xml"

    PDP_sitemaps = get_pdp_sitemaps(master)

    all_links = []
    for xml_page in PDP_sitemaps:
            sub_links = extract_links(xml_page)
            all_links.extend(sub_links)

    output_path = '/Users/cristinconnerney/Desktop/Instalily/data/links.txt'

    with open(output_path,'w') as outfile:
        outfile.writelines(all_links)

if __name__ == '__main__':
    main()
    