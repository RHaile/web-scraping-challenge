from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    mars_data = {}

    # Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_news = soup.find("div", class_="list_text")
    news_title = latest_news.find("div", class_="content_title").text
    news_p = latest_news.find("div", class_="article_teaser_body").text
  
    mars_data["title"] = news_title
    mars_data["summary"] = news_p



    # JPL's Space Image 
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image

    mars_data["featured_image"] = featured_image_url


    # Mars Weather 
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = tweet.find('p','tweet-text').get_text()
    
    mars_data["weather"] = mars_weather


    # Mars Facts
    url_facts = "https://space-facts.com/mars/"

    mars_df = pd.read_html(url_facts)[0]
    mars_df.columns=['description', 'value']
    mars_df.set_index('description', inplace=True)

    mars_table = mars_df.to_html(classes="table table-striped")
    mars_table = mars_table.replace('\n', ' ')

    mars_data["facts"] = mars_table


    # Mars Hemispheres
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)

    mars_hemispheres = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        urls_titles = {}
    
        browser.find_by_css("a.product-item h3")[i].click()
        anchor_tag = browser.find_link_by_text('Sample').first
    
        urls_titles['img_url'] = anchor_tag['href']
        urls_titles['title'] = browser.find_by_css("h2.title").text
    
        mars_hemispheres.append(urls_titles)
    
        browser.back()

    mars_data['hemispheres'] = mars_hemispheres

    browser.quit()
    return mars_data
