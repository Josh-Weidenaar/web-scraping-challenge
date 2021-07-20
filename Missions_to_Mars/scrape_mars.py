import pandas as pd
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

def scrape():
    dictie = {}
    p_class_target = "article_teaser_body"
    headline_target = "content_title"

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.is_element_visible_by_css('div[class="list_text"]',wait_time=10)
    browser.visit(url)


    page = browser.html
    soup = BeautifulSoup(page, 'html.parser')

    soup

    news_title = soup.find("div",{"class": headline_target})
    news_p = soup.find("div",{"class": p_class_target})

    news_p = news_p.text
    news_title = news_title.text
    
    
    dictie['news_title'] = news_title
    dictie['news_p'] = news_p
    
    url = "https://spaceimages-mars.com"
    browser.visit(url)

    browser.click_link_by_partial_href('image/featured/')

    img = browser.html
    soup = BeautifulSoup(img, 'html.parser')

    href = soup.find("img",{"class": "fancybox-image"})['src']

    url = browser.url

    url

    imgurl = url + href

    dictie['featured_image_url'] = imgurl

    df = pd.read_html("https://galaxyfacts-mars.com")
    html_table_string = pd.DataFrame(df[1]).to_html()
    
    
    dictie['fact_table'] = html_table_string
    
    
    hemisphere_image_urls = []
    url = "https://marshemispheres.com/"
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    # browser.visit(url)

    # browser.click_link_by_partial_text('Hemisphere')
    # for i in link:
    #     dct = {}
    #     keys = ['title','img_url']

    soup_list = soup.find_all('div',attrs={'class':'item'})
    url_list = []
    for i in soup_list:
        href = i.find("a",attrs={'class':'itemLink'})['href']
        url_list.append(url + href)


    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')


    url_list

    for i in url_list:
        dct = {}
        html = requests.get(i)
        soup = BeautifulSoup(html.content,'html.parser')
        title_target = 'h2'
        img_url_target = 'a'
        img_url_target_text = 'Sample'
        base = "https://marshemispheres.com/"
        keys = ['title','img_url']
        dct[keys[0]] = soup.find(title_target).text
        dct[keys[1]] = base + soup.find(img_url_target,text=img_url_target_text)['href']
        hemisphere_image_urls.append(dct)


    dictie['hemisphere_image_urls'] = hemisphere_image_urls
    return dictie