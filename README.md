# Jcrew Bot

## Files

Web Scraping:
* Get_links: Save links for all PDPs.
* Product_scraper: Extract relevant information from a single product page. 
* Scraper_main: Scrapes pages using Product_scraper and iteratively save to csv. 

Chatbot:
* Index: Create embeddings and store in a vectorstore. 
* Chat: Load vectorstore, set up langchain, run streamlit app

