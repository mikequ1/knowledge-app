import requests 
from bs4 import BeautifulSoup 
import random
import wikipedia

topics = ["Communism", "Abortion", "Black Lives Matter", "Gun Control", "Climate Change", "Immigration", "Death Penalty", "Torture", "Andriod vs IOS", "Government Control", 
        "U.S leave the middle east", "Best Sandwich", "Do IVY league matters", "Laws against Hate Speech", "Affirmative action", "Fracking", "defunding police", "marijuanas",
        "Socialsim vs Capitalism"]

wikipedia_link = "https://en.wikipedia.org/wiki/"

def choose_topics():
    topic = random.choice(topics)
    get_wikipedia(topic)


def get_wikipedia(topic):
    #Get page of Wikipedia topic to get the title 
    topic_start = wikipedia.page(topic)
    print(topic_start.title)

    #Get URL from Wikipedia Topic 
    print(topic_start.url)

    #Get a quick summary of the topic
    print (wikipedia.summary(topic))
    



choose_topics()