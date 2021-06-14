#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': '/Users/jocel/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# # NASA Mars News

# In[3]:


##Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.


# In[4]:


url = "https://redplanetscience.com/"
browser.visit(url)


# In[5]:


html = browser.html
soup = bs(html, 'html.parser')


# In[6]:


#Search
title_search = soup.find_all('div', class_= 'content_title')
p_search = soup.find_all('div', class_='article_teaser_body')


# In[7]:


#Collect Title and Paragraph Text and assign variables
news_title = title_search[0].text
news_p = p_search[0].text
print(news_title)
print(news_p)


# # JPL Mars Space Images - Featured Image

# In[8]:


##Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called


# In[9]:


browser.visit('https://spaceimages-mars.com/')


# In[10]:


browser.links.find_by_partial_text('FULL IMAGE')


# In[11]:


html = browser.html
soup = bs(html, 'html.parser')


# In[12]:


# Search for image source

feature_image = soup.find('img', class_='headerimage fade-in')

feature_image_path = feature_image.get('src')

featured_image_url = 'https://spaceimages-mars.com/' + feature_image_path 

print(featured_image_url)


# # Mars Facts

# In[13]:


##Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc


# In[14]:


url_facts = "https://galaxyfacts-mars.com"


# In[15]:


mars_table = pd.read_html(url_facts)


# In[16]:


mars_df =mars_table[1]


# In[17]:


mars_df.columns=['description','value']
mars_df.head(5)


# In[18]:


##Use Pandas to convert the data to a HTML table string.


# In[19]:


mars_facts_table = [mars_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
mars_facts_table


# # Mars Hemispheres
# 
# 
# 

# In[20]:


##Obtain high resolution images for each of Mar's hemispheres.
##Use a Python dictionary to store the data using the keys img_url and title.


# In[21]:


url_hem = "https://marshemispheres.com/"
browser.visit(url_hem)


# In[22]:


html = browser.html
soup = bs(html, 'html.parser')


# In[23]:


#Search for Mars Hemisphere Titles
mars_hem = []
hem_search = soup.find_all('div', class_="collapsible results")
hemispheres = hem_search[0].find_all('h3')

for title in hemispheres:
    mars_hem.append(title.text)
    
mars_hem


# In[24]:


#Search for links to Hemisphere Images
image_search = hem_search[0].find_all('a')
image_links = []

for image in image_search:
    if (image.img):
        
        image_url = 'https://marshemispheres.com/' + image['href']
        
        image_links.append(image_url)

image_links


# In[25]:


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

full_images
    


# In[26]:


#Store as list of Dictionaries


# In[27]:


mars_hemispheres = zip(mars_hem, full_images)

mars_hemispheres_image_urls = []

for title, image in mars_hemispheres:
    
    mars_hemispheres_dict = {}
    
    mars_hemispheres_dict['title'] = title
    
    mars_hemispheres_dict['image_url'] = image
    
    mars_hemispheres_image_urls.append(mars_hemispheres_dict)
    
mars_hemispheres_image_urls

