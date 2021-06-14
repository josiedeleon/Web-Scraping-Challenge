import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests

def init_browser():
	executable_path = {'executable_path': '/Users/jocel/chromedriver'}
	return Browser('chrome', **executable_path, headless=False)

def scrape(): #NASA Mars News

##Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
browser = init_browser()
url = "https://redplanetscience.com/"
browser.visit(url)

html = browser.html
soup = bs(html, 'html.parser')

#Search
title_search = soup.find_all('div', class_= 'content_title')
p_search = soup.find_all('div', class_='article_teaser_body')

#Collect Title and Paragraph Text and assign variables
news_title = title_search[0].text
news_p = p_search[0].text

##JPL Mars Space Images - Featured Image
##Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called
browser.visit('https://spaceimages-mars.com/')
browser.links.find_by_partial_text('FULL IMAGE')
html = browser.html
soup = bs(html, 'html.parser')

# Search for image source
feature_image = soup.find('img', class_='headerimage fade-in')
feature_image_path = feature_image.get('src')
featured_image_url = 'https://spaceimages-mars.com/' + feature_image_path 

##Mars Facts
#Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
url_facts = "https://galaxyfacts-mars.com"
mars_table = pd.read_html(url_facts)
mars_df =mars_table[1]

mars_df.columns=['description','value']

##Use Pandas to convert the data to a HTML table string.
mars_facts_table = [mars_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
mars_facts_table

##Mars Hemispheres
##Obtain high resolution images for each of Mar's hemispheres.
##Use a Python dictionary to store the data using the keys img_url and title.

url_hem = "https://marshemispheres.com/"
browser.visit(url_hem)
html = browser.html
soup = bs(html, 'html.parser')

#Search for Mars Hemisphere Titles
mars_hem = []
hem_search = soup.find_all('div', class_="collapsible results")
hemispheres = hem_search[0].find_all('h3')

for title in hemispheres:
    mars_hem.append(title.text)
    
#Search for links to Hemisphere Images
image_search = hem_search[0].find_all('a')
image_links = []

for image in image_search:
    if (image.img):
        
        image_url = 'https://marshemispheres.com/' + image['href']
        
        image_links.append(image_url)
#Extract Image Sources for full-sized pictures

full_images = []

for url in image_links:
    
    browser.visit(image_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    images = soup.find_all('img', class_='wide-image')
    image_path = images[0]['src']
    
    image_link = 'https://marshemispheres.com/' + image_path
    
    full_images.append(image_link)
#Store as list of Dictionaries
mars_hemispheres = zip(mars_hem, full_images)

mars_hemispheres_image_urls = []

for title, image in mars_hemispheres:
    
    mars_hemispheres_dict = {}
    
    mars_hemispheres_dict['title'] = title
    
    mars_hemispheres_dict['image_url'] = image
    
    mars_hemispheres_image_urls.append(mars_hemispheres_dict)
    

mars_info = {
        "mars_news": {
            "news_title": news_title,
            "news_p": news_p,
            },
        "mars_img": featured_image_url,
        "mars_fact": mars_df,
        "mars_hemisphere": mars_hemisphere_image_urls
    }
    
  browser.quit()

    return mars_info