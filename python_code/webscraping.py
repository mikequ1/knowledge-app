# Program grabs wikipedia series and inputs all links into a json file. 
import requests 
import json 
from bs4 import BeautifulSoup
from googlesearch import search
import wikipedia
import os
from time import sleep
from simple_image_download import simple_image_download as simp 

topics = ["EWFfsdf", "Communism", "Discrimination", "Capitalism", "Bioethics", 
        "War", "Education", "Genetic engineering", "Climate Change", 
        "Human overpopulation", "Artificial intelligence", "Pharmaceutical industry", "Computer security", "Mental health"]

global_links = []

wikipedia_link = "https://en.wikipedia.org/wiki"  

def get_wikipedia_scraping(topic): 
    error_string = "Wikipedia does not have an article with this exact name."
    # Request for Wikipedia link on the topic
    page = requests.get(wikipedia_link + "/" + topic)
    page_info = BeautifulSoup(page.content, features="lxml")

    try: 
        # Check if Wikipedia topic exists
        for error in page_info.findAll('b'):
            if error_string in error.text.strip():
                return 0

        # Grab the URL from the Wikipedia Page
        get_url = page.url
        global_links.append(get_url)

        #Check other sources for links 
        input_links(page_info)
        check_series_links(topic)

        page.close()
        return 1

    # return Zero if an Index Error occurs
    except requests.exceptions.ConnectionError: 
        sleep(300)
        global_links.clear()
        get_wikipedia_scraping(topic)


def get_wikipedia_title(topic): 
    try: 
        page = requests.get(topic)
        page_info = BeautifulSoup(page.content, features="lxml")
        
        # grabs the title of the wikipedia article
        title = page_info.find_all("h1", class_="firstHeading")
        page.close()
        return title[0].text.strip()
    
    except requests.exceptions.ConnectionError: 
        sleep(300)
        get_wikipedia_title(topic)


def check_json(json_line):
    # checks if there is a duplicate or not
    for title in json_line:
        for topic in topics:
            if topic.lower() == title["Topic"].lower():
                print(topic)
                topics.remove(topic)
                

def input_links(page_info):
    # checks if there are links to the right side of the main article 
    try: 
        for get_side_links in page_info.find_all('div', class_= "sidebar-list-content mw-collapsible-content"):
            for namelink in get_side_links.find_all("li"):
                global_links.append("https://en.wikipedia.org" + namelink.a['href'])

    except requests.exceptions.ConnectionError:
        raise
    
    except: 
        print("No side links")


def check_series_links(topic):
    # checks if there is a series for the article 
    try: 
        page = requests.get(wikipedia_link + "/" + "Category:" + topic)
        page_info = BeautifulSoup(page.content, features="lxml")
        for series_links in page_info.find_all("div", class_= "mw-category"):
            for link in series_links.find_all("li"):
                if str(link).find("/Category:") == -1:
                    global_links.append("https://en.wikipedia.org" + link.a['href'])
        
        page.close()

    except requests.exceptions.ConnectionError: 
        raise

    except: 
        print("No series")

def get_picture_link(topic): 
    # grabs pictures 
    r = requests.get("https://www.google.com/search?q=" + topic + "&safe=strict&rlz=1C1CHBF_enUS925US925&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjSgNaHzszvAhUHKK0KHTltDj8Q_AUoAnoECAEQBA&biw=1268&bih=589")
    soup = BeautifulSoup(r.content, features="lxml")
    # look for picture links on google and return them
    for link in soup.select("img[src^=http]"):
        if "http" in link.get('src'):
            lnk = link.get('src')
            return lnk
    
    r.close()

def get_summary(url): 
    try: 
        # replaces the wikipedia url to get the article summary
        if url.find("https://en.wikipedia.org/wiki/") != -1:
            y = url.replace('https://en.wikipedia.org/wiki/', '')
            return wikipedia.summary(y)

    except requests.exceptions.ConnectionError:
        sleep(300)
        get_summary(url)
        
    except: 
        return "No Summary Available"


def write_json(data, filename='wiki_info.json'):
    with open(filename,'w') as f:
        # Import all data into json file
        json.dump(data, f, indent=4)


if __name__ == '__main__':  
    with open('wiki_info.json') as json_file:

        # Ask the user if they want to add topics
        ans = input("Do you want to add more topics (Enter 1 for yes or 2 for no?): ")
        while ans == "1": 
            add_topic = input("Add one topic: ")
            topics.append(add_topic.lower())

            ans = input("Do you wish to add another topic? (Enter 1 for yes or 2 for no?): ")
            
        # Load the json file to be readable by python
        data = json.load(json_file)
        temp = data["Topics"]

        # check whether the topic has been used
        check_json(temp)
        
        for topic in topics:
            # Grab Wikipedia information
            check = get_wikipedia_scraping(topic)
            
            # Checks whether there is any information on topic 
            if check == 0:
                continue
            else: 
                # Goes through URLS in the global_url and attaches to json
                for url in global_links:
                    # Grab title of the current article 
                    title = get_wikipedia_title(url)

                    add_json = { 
                        "Topic" : topic, 
                        "Site": [{
                            "Title": title, 
                            "Summary": get_summary(url),  
                            "Url": url,
                            "Pictures" : get_picture_link(title)
                        }]
                    }

                    # append to the current copied json
                    temp.append(add_json)

                    # Write to json 
                    write_json(data)
                # Clear list for next topic links
                global_links.clear()

            