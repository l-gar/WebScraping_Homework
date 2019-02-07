#!/usr/bin/env python
# coding: utf-8

#import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
# from env import get_pymongo_conn

def scrape():

        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)

        mars_data = {}

        #url and get page request
        mars_url = 'https://mars.nasa.gov/news/'
        browser.visit(mars_url)
        # response = requests.get(mars_url)
        html = browser.html
        mars_soup = BeautifulSoup(html, 'html.parser')

        news_title = mars_soup.find('div', class_='content_title').text.strip()
        news_p = mars_soup.find('div', class_='rollover_description_inner').text.strip()
        print(news_title)
        print(news_p)

        mars_data["news_title"] = news_title
        mars_data["summary"] = news_p



        # get this 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22959_hires.jpg'
        #soup.find("span", {"class": "real number", "data-value": True})['data-value']
        mars_url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(mars_url2)
        html_image = browser.html
        mars_soup = BeautifulSoup(html_image, "html.parser")

        base_url = 'https://www.jpl.nasa.gov'

        img = mars_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        #mars_soup.find('div', class_='image_and_description_container').find('div', class_='list_image').img['src']

        featured_img_url = f'{base_url}{img}'
        print(featured_img_url)

        mars_data['featured_image'] = featured_img_url

        mars_url3 = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(mars_url3)
        html_tweet = browser.html
        mars_soup = BeautifulSoup(html_tweet, 'html.parser')

        mars_weather_tweet = mars_soup.find_all('div', class_='js-tweet-text-container')

        for tweet in mars_weather_tweet:
                if tweet.text.strip().startswith('Sol'):
                        mars_weather = tweet.text.strip()
                        break
        print(mars_weather)

        mars_data['mars_weather'] = mars_weather

        mars_url4 = 'https://space-facts.com/mars/'
        facts_data = pd.read_html(mars_url4)
        facts_data[0]

        facts_df = facts_data[0]
        facts_df.columns = ['Attribures','Values']
        facts_df.head()
        mars_tb = facts_df.set_index('Attribures')
        marsinfo = mars_tb.to_html()
        marsinfo = marsinfo.replace('\n', ' ')

        # Add the Mars facts table to the dictionary
        mars_data["mars_table"] = marsinfo

        mars_url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(mars_url4)
        html_hem = browser.html
        mars_soup = BeautifulSoup(html_hem, 'html.parser')
        mars_hemispheres = []

        for x in range(4):
                image1 = browser.find_by_tag('h3')
                image1[x].click()
                html_hem = browser.html
                mars_soup = BeautifulSoup(html_hem, 'html.parser')
                img_baseurl = 'https://astrogeology.usgs.gov'
                img_partial1 = mars_soup.find('img', class_='wide-image')['src']
                img_title1 = mars_soup.find('h2', class_='title').text.strip()
                img_url1 = f'{img_baseurl}{img_partial1}'
                dic = {'Title': img_title1, 'url': img_url1}
                mars_hemispheres.append(dic)
                browser.back()

        print(mars_hemispheres)
        mars_data['mars_hemispheres'] = mars_hemispheres

        return mars_data





