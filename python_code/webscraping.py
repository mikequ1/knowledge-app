import requests 
import json 
from bs4 import BeautifulSoup
from googlesearch import search


link_filter = ["en.wikipedia.org", "climate.nasa.gov", "www.history.com", "www.brookings.edu", "www.britannica.com", 
            "deathpenaltyinfo.org", "harvardpolitics.com", "www.nrdc.org", "www.livescience.com", "www.epa.gov", "www.nrdc.org",
            "www.nature.org", "news.gallup.com", "www.pewresearch.com", "www.foundationsoflife.org", "prochoice.org",
            "www.plannedparenhood.org", "www.investopedia.com"]

topics = ["Communism", "Abortion", "Black Lives Matter", "Gun Control", "Climate Change", "Immigration", "Death Penalty", "Torture", "Andriod vs IOS", "Government Control", 
        "U.S leave the middle east", "Best Sandwich", "Do IVY league matters", "Laws against Hate Speech", "Affirmative action","defunding police", "marijuanas",
        "Socialsim vs Capitalism", "Fracking"]

wikipedia_link = "https://en.wikipedia.org/wiki/"
      
def get_topics_json():     
    with open('wiki_info.json') as json_file:
        data = json.load(json_file)
      
        temp = data["Topic"]

        # Check for duplicates in json file 
        for json_line in temp:
            check_json(json_line["Name"])

        # Make new json elements and add them
        for topic in topics:
            json_info = get_wikipedia_scraping(topic)

            #Continue if json_info has a return of 0
            if json_info == 0:  
                continue
            else:
                all_links = get_links(topic, json_info[2])

                # Input all links in list[2]
                for link in all_links: 
                    json_info[2] = json_info[2] + " " + str(link) 

                # Add collected info into json element
                add_json = {
                    "Name": topic,
                    "Title": json_info[0],  
                    "Summary": json_info[1],
                    "URL": json_info[2], 
                }
            
                # Append to json
                temp.append(add_json)
        write_json(data)

def get_links(topic, url_used):
    links = []
    
    # Grab 20 Search results 
    for google_link in search(topic, tld="co.in", num=20, stop=20, pause=1):
        # Check the link off link filter and append to list
        for selected_link in link_filter: 
            if google_link.find(selected_link) != -1:
                if url_used in selected_link: 
                    continue
                else:  
                    links.append(google_link)

    return links
    

def get_wikipedia_scraping(topic): 
    info = []
    
    # Request for Wikipedia link on the topic
    page = requests.get(wikipedia_link + topic)
    page_info = BeautifulSoup(page.content, features="lxml")

    try: 
        # Grab the title of the Wikipedia Page 
        title = page_info.find_all("h1", class_="firstHeading") 
        info.append(title[0].text.strip())

        # Grab a summary from the Wikipedia Page
        summary = page_info.find_all('div', class_="shortdescription nomobile noexcerpt noprint searchaux")
        info.append(summary[0].text.strip())

        # Grab the URL from the Wikipedia Page
        get_url = page.url
        info.append(get_url)

        #Check other sources for links 
        input_links(page_info, info)
        check_series_links(page_info, info, topic)
        print(info[2])

    # return Zero if an Index Error occurs
    except IndexError: 
        return 0 
    
    # Return list of Wikipedia information
    return info


def check_json(json_line):
    # Delete from topics list if there is a duplicate
    for topic in topics:
        if json_line in topic:
            topics.remove(topic)


def input_links(page_info, info):
    try: 
        for get_side_links in page_info.find_all('div', class_= "sidebar-list-content mw-collapsible-content"):
            for namelink in get_side_links.find_all("li"):
                info[2] = info[2] + " " + wikipedia_link + namelink.a['href']
    
    except: 
        print("No side links")


def check_series_links(page_info, info, topic):
    try: 
        page = requests.get(wikipedia_link + "Category:" + topic)
        page_info = BeautifulSoup(page.content, features="lxml")

        for series_links in page_info.find_all("div", class_= "mw-category"):
            for link in series_links.find_all("li"):
                if str(link).find("/Category:") == -1: 
                    info[2] = info[2] + " " + wikipedia_link + link.a['href']

    except: 
        print("No series")
        
def write_json(data, filename='wiki_info.json'):
    with open(filename,'w') as f:
        # Import all data into json file
        json.dump(data, f, indent=4)

get_topics_json()