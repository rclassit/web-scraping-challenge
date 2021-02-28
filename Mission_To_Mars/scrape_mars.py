#Importing Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def mars_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = mars_browser()
    mars_list = {}

    #mars news scrape
    browser.visit('https://mars.nasa.gov/news/')
    html = browser.html
    news_soup = bs(html, 'html.parser')
    news_title = browser.find_by_css('div.content_title a')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    #Mars image scrape


    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    image = browser.find_by_css('img.fancybox-image')['src']
    featured_image_url = image

    #Mars Facts scrape
    Mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(Mars_facts_url)
    mars_df = tables[2]
    mars_df.columns = ['Description','Value']
    mars_html = mars_df.to_html()
    mars_html.replace('\n','')

    #Mars Hemisphere name and image scrape
    main_url = 'https://astrogeology.usgs.gov'
    hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres)
    hemispheres_html = browser.html
    hemi_soup = bs(hemispheres_html, 'html.parser')
    all_hemispheres= hemi_soup.find('div',class_ = 'collapsible results')
    mars_hemi = all_hemispheres.find_all('div',class_='item')
    hemi_images = []
    #for loop for hemi data
    for i in mars_hemi:
        #title
        hemisphere = i.find('div', class_ ="description")
        title = hemisphere.h3.text
        
        #Image link
        hemisphere_url = hemisphere.a["href"]
        browser.visit(main_url + hemisphere_url)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_ ='downloads')
        image_url = image_link.find('li').a['href']
        
        #Dictionary Storage
        images = {}
        images['title'] = title
        images['image_url'] = image_url
        hemi_images.append(images)
    
    #Mars list
    mars_list = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_facts" : str(mars_html),
        "hemisphere_images" : hemi_images
    }

    return mars_list



