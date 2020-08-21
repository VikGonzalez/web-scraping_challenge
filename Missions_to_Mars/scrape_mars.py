# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import time
import re
import pandas as pd

def scrape():

    # Google ChromeDriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

    # Google chrome browser
    browser = Browser("chrome", **executable_path, headless=False)

    # NASA Mars News Site
    browser.visit("https://mars.nasa.gov/news/")
    time.sleep(3)

    # HTML into a Beautiful Soup
    nasaNewsHTML = browser.html
    soup = bs(nasaNewsHTML,"html.parser")

    # latest headlines
    news_title = soup.find_all("div",class_="content_title", limit=2)[1].text
    news_p = soup.find("div",class_="article_teaser_body").text

    # Results
    print(f"{news_title}")
    print(f"------------")
    print(f"{news_p}")

    # JPL Space Images website
    jplImages = "https://www.jpl.nasa.gov"
    browser.visit(f"{jplImages}/spaceimages/?search=&category=Mars")

    # HTML into a Beautiful Soup
    jplHTML = browser.html
    soup = bs(jplHTML,"html.parser")

    # URL data from soup
    bgImage = soup.find("article",class_="carousel_item").get('style')

    # local URL
    URL = bgImage.split("'")[1]

    # Explicit featured image URL
    featured_image_url = jplImages + URL

    # Image URL
    print(featured_image_url)

    # Browse @MarsWxReport Twitter Account
    marsTwitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsTwitter)
    time.sleep(5)

    # HTML into a Beautiful Soup
    twitter = browser.html
    soup = bs(twitter,"lxml")

    # latest mars weather
    InSight = soup.find(text=re.compile('InSight sol'))

    # Format
    mars_weather = InSight.replace('InSight sol', 'Sol', 1)

    # Results
    print(mars_weather)

    # Mars Facts website
    marsFacts = "https://space-facts.com/mars/"

    # Tabels contained in URL
    tables = pd.read_html(marsFacts)

    # Obtained table
    factTable = tables[0].set_index(0)

    # Table as HTML
    factTable.to_html(os.path.join(".","templates/fact_table.html"), header=False, index_names = False)

    # Mars Astrogeology page
    marsHemis = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marsHemis)

    # HTML into a Beautiful Soup
    hemis = browser.html
    soup = bs(hemis,"lxml")

    # Pull links
    results = soup.find_all("a", class_="itemLink product-item")

    # list of unique weblinks
    hemiLinks = []
    for item in results:
        if item.get('href') not in hemiLinks:
            hemiLinks.append(item.get('href'))

    # Close browser
    browser.quit()
    
    # USGS URL 
    usgs_url = 'https://astrogeology.usgs.gov'

    # list
    hemisphere_image_urls = []

    for link in hemiLinks:
        hemisphere_dict = {}
        browser = Browser("chrome", **executable_path, headless=False)
        browser.visit(usgs_url+link)
        hemi_i = browser.html
        soup = bs(hemi_i,"lxml")
        hemisphere_dict['title'] = soup.find('h2',class_="title").text.replace(' Enhanced','')
        hemisphere_dict['img_url'] = soup.find('div', class_='downloads').a.get('href')
        hemisphere_image_urls.append(hemisphere_dict)
        browser.quit()

        # Results
        print(hemisphere_image_urls)

    # dictionary
    results = {
        'news_title' : news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather' : marsTwitter,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return results