import requests 
from bs4 import BeautifulSoup 

topics = [] 
wikipedia_link = "https://en.wikipedia.org/wiki/"

def wiki_scraping(topic): 
    page = request.get(wikipedia_link + topic).content 

    javascript_info = BeautifulSoup(page, features='lxml')
    article = info.find_all()

