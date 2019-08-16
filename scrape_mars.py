from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    
def load_browser(url,browser):
    
    
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Close the browser after scraping
    #browser.quit()
    return soup
def get_image_info(soup):
    # Get image URL
    image_info = soup.find(class_="downloads")
    image_info_link = image_info.find("li").find("a")
    img_url = image_info_link.get("href")

    # Get hemisphere title
    title = soup.find(class_="content").find(class_="title").text

    # Create dict object
    mars_hemi_dict = {}
    mars_hemi_dict["title"] = title
    mars_hemi_dict["img_url"] = img_url

    return mars_hemi_dict


def scrape_info():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    soup = load_browser(url,browser)
    title_div = soup.find('div', class_='content_title').text
    p_div = soup.find('div' , class_ = 'article_teaser_body').text
    print(f'{title_div}\n{p_div}')
    base_url = "https://www.jpl.nasa.gov"
    soup = load_browser(base_url + "/spaceimages/?search=&category=Mars",browser)
    featured_image = soup.find(class_ = 'carousel_item')
    featured_image_a = featured_image.find('a')
    featured_image_link =featured_image_a.get('data-fancybox-href') 
    featured_image_link = base_url+featured_image_link
    print(f'Link for the featured image(Mars) \n{featured_image_link}')
    
    # Mars Weather latest tweet
    twitter_base_url = 'https://twitter.com/marswxreport?lang=en'
    soup = load_browser(twitter_base_url,browser)
    mars_weather_tweets = soup.find_all('p',class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    for tweet in mars_weather_tweets:
        weather_tweet = tweet.text
        if(weather_tweet.startswith('InSight sol')):
            mars_weather = weather_tweet
            break
    print(mars_weather)

    #Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    planet_facts = tables[1]
    print(planet_facts)

    # converting to html table
    facts_html_string = planet_facts.to_html(justify="left",index=False,header=False)
    print(facts_html_string)

    #
    base_url = 'https://astrogeology.usgs.gov'
    mars_hemi_url = base_url + '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    soup = load_browser(mars_hemi_url,browser)
    links = []
    parents = soup.select("#results-accordian")    
    for parent in parents :
        
        for x in range(0,8, 2):
            a = parent.select('a',class_ = 'itemLink product-item')[x]
            links.append(base_url + a.get("href"))
    mars_hemi_info = []
    for link in links:
        soup = load_browser(link,browser)
        mars_hemi_info.append(get_image_info(soup))
        
    print(mars_hemi_info)
    # Store data in a dictionary
    mars_data = {
        "title": title_div,
        "description": p_div,
        "image_link" : featured_image_link,
        "mars_weather" : mars_weather,
        "mars_facts" : facts_html_string,
        "hemi_links" : mars_hemi_info
    }
    print(mars_data['hemi_links'])

    # Return results
    return mars_data

    
