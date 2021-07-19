from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

#
def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # browser.visit(url)
    # browser.visit(url)
    # browser.visit(url)
    # browser.visit(url)
    
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the latest news
    results = soup.find_all('div', class_='list_text')

    news = {"headline":[],"paragraph":[]}
        
    for result in results[:1]:
    
        headline = result.find('div', class_='content_title').text
        paragraph = result.find('div', class_='article_teaser_body').text
        news['headline'].append(headline)
        news['paragraph'].append(paragraph)
    
    #Get the featured image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Store image in variables
    image_url = "https://spaceimages-mars.com/"+soup.find('img', class_='headerimage fade-in')['src']


    # Get Mars facts
    url = 'https://galaxyfacts-mars.com'

    # Read html tables
    tables = pd.read_html(url)

    # Create dataframe from table
    df = tables[0]
  
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    
    # Convert dataframe to html table, and store as variable
    html_table = df.to_html(index = False)

    # Get Mars Hemisphere images
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    collapsible = soup.find('div',class_="collapsible")
    hemisphere_image_urls = []

    for i in range(0,4):
    
        hemi_dict = {}
        hemi_dict['title'] = collapsible.find_all("h3")[i].text
        html_link = 'https://marshemispheres.com/'+str(collapsible.find_all('a', class_="itemLink product-item")[i*2]['href'])
        browser.visit(html_link)
        hemi_soup = BeautifulSoup(browser.html, 'html.parser')
        hemi_dict['image_url'] = 'https://marshemispheres.com/'+str(hemi_soup.find('img', class_='wide-image')['src'])
        hemisphere_image_urls.append(hemi_dict)


    # # Quit the browser after scraping
    browser.quit()

    scraped_data = {
        "news":news, 
        "featured_image": image_url,
        "html_table": html_table,
        "hemisphere": hemisphere_image_urls

    }
    # Return results
    return scraped_data