import requests 
import json 
from bs4 import BeautifulSoup
from googlesearch import search
import wikipedia
import os
from time import sleep
from simple_image_download import simple_image_download as simp 


link_filter = ["en.wikipedia.org"]

link_filter_two = ["climate.nasa.gov", "www.history.com", "www.brookings.edu", "www.britannica.com", 
            "deathpenaltyinfo.org", "harvardpolitics.com", "www.nrdc.org", "www.livescience.com", "www.epa.gov", "www.nrdc.org",
            "www.nature.org", "news.gallup.com", "www.pewresearch.com", "www.foundationsoflife.org", "prochoice.org",
            "www.plannedparenhood.org", "www.investopedia.com"]

topics = ["r5u6it7kligrd", "Communism", "Discrimination", "Capitalism", "Bioethics", 
        "War", "Education", "Genetical Modified Organsim", "Climate Change", 
        "Human overpopulation", "Artificial Intelligence", "Pharmaceutical industry", "Cybersecurity", "Mental Health", "History"]

global_links = []

wikipedia_link = "https://en.wikipedia.org/wiki"  

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
    page = requests.get(wikipedia_link + "/" + topic)
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
        global_links.append(get_url)

        #Check other sources for links 
        input_links(page_info)
        check_series_links(topic)

        page.close()
        return 1

    except requests.exceptions.ConnectionError:
        sleep(120)
        # Grab the title of the Wikipedia Page 
        title = page_info.find_all("h1", class_="firstHeading") 
        info.append(title[0].text.strip())

        # Grab a summary from the Wikipedia Page
        summary = page_info.find_all('div', class_="shortdescription nomobile noexcerpt noprint searchaux")
        info.append(summary[0].text.strip())

        # Grab the URL from the Wikipedia Page
        get_url = page.url
        global_links.append(get_url)

        #Check other sources for links 
        input_links(page_info)
        check_series_links(topic)

        page.close()
        return 1

    # return Zero if an Index Error occurs
    except IndexError: 
        page.close()
        return 0 
    


def get_wikipedia_title(topic): 
    page = requests.get(topic)
    page_info = BeautifulSoup(page.content, features="lxml")

    title = page_info.find_all("h1", class_="firstHeading")
    page.close()
    return title[0].text.strip()


def check_json(json_line):
    # Delete from topics list if there is a duplicate
    for topic in topics:
        if json_line in topic:
            topics.remove(topic)


def input_links(page_info):
    try: 
        for get_side_links in page_info.find_all('div', class_= "sidebar-list-content mw-collapsible-content"):
            for namelink in get_side_links.find_all("li"):
                global_links.append("https://en.wikipedia.org" + namelink.a['href'])
    except requests.exceptions.ConnectionError:
        sleep(120)
        for get_side_links in page_info.find_all('div', class_= "sidebar-list-content mw-collapsible-content"):
            for namelink in get_side_links.find_all("li"):
                global_links.append("https://en.wikipedia.org" + namelink.a['href'])
    except: 
        print("No side links")


def check_series_links(topic):
    try: 
        page = requests.get(wikipedia_link + "/" + "Category:" + topic)
        page_info = BeautifulSoup(page.content, features="lxml")
        for series_links in page_info.find_all("div", class_= "mw-category"):
            for link in series_links.find_all("li"):
                if str(link).find("/Category:") == -1:
                    global_links.append("https://en.wikipedia.org" + link.a['href'])
        
        page.close()
    except requests.exceptions.ConnectionError:
        sleep(120)
        page = requests.get(wikipedia_link + "/" + "Category:" + topic)
        page_info = BeautifulSoup(page.content, features="lxml")
        for series_links in page_info.find_all("div", class_= "mw-category"):
            for link in series_links.find_all("li"):
                if str(link).find("/Category:") == -1:
                    global_links.append("https://en.wikipedia.org" + link.a['href'])

    except: 
        print("No series")

def get_picture_link(topic): 
    r = requests.get("https://www.google.com/search?q=" + topic + "&safe=strict&rlz=1C1CHBF_enUS925US925&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjSgNaHzszvAhUHKK0KHTltDj8Q_AUoAnoECAEQBA&biw=1268&bih=589")
    soup = BeautifulSoup(r.content, features="lxml")

    for link in soup.select("img[src^=http]"):
        if "http" in link.get('src'):
            lnk = link.get('src')
            return lnk
    
    r.close()

def get_directory(topic): 
    dir_path = os.listdir("simple_images")

    for i in dir_path:
        i = i.replace(' ', '_')
        topic = topic.replace(' ', '_')
        if i == topic:
            y = os.listdir("simple_images/" + i)
            for x in y: 
                return x

def get_summary(url): 
    try: 
        if url.find("https://en.wikipedia.org/wiki/") != -1:
            y = url.replace('https://en.wikipedia.org/wiki/', '')
            return wikipedia.summary(y)
    except requests.exceptions.ConnectionError:
        sleep(120)
        if url.find("https://en.wikipedia.org/wiki/") != -1:
            y = url.replace('https://en.wikipedia.org/wiki/', '')
            return wikipedia.summary(y)
    except: 
        return "No Summary Available"


def write_json(data, filename='wiki_info.json'):
    with open(filename,'w') as f:
        # Import all data into json file
        json.dump(data, f, indent=4)


if __name__ == '__main__':  
    with open('wiki_info.json') as json_file:

        data = json.load(json_file)
        temp = data["Topics"]

        for topic in topics:
            # Sleep when wikipedia closes connection
            try: 
                check = get_wikipedia_scraping(topic)
            except requests.exceptions.ConnectionError: 
                sleep(300)
                global_links.clear()
                check = get_wikipedia_scraping(topic)
                continue
            
            # Checks whether there is any information on topic 
            if check == 0:
                continue
            else: 
                # Goes through URLS in the global_url and attaches to json
                for url in global_links:
                        sleep(3)
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
                
                        temp.append(add_json)

                        write_json(data)
                # Clear list for next topic links
                global_links.clear()

            