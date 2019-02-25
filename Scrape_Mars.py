

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

from selenium import webdriver
    # a note here with the dependencies, I was unable to access my twitter account with splinter, and decided to use 
    # Selenium Webdriver instead 

    # first up Mars News
def scrape():
    
    Response = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    Nasa = Response.text
    soup = bs(Nasa,'html.parser')
    Mars_News_Title = soup.title.text.strip()
    Mars_News_Text = soup.body.p.text

    # Nasa Image
    browser = webdriver.Chrome('chromedriver')
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.get(url)
    elem = browser.find_element_by_id('full_image')
    elem.click()
    html = browser.page_source
    soup2 = bs(html, 'html.parser')
    full_image = str(soup2.find_all('img',class_='fancybox-image'))
    full_image_url = url[:-22]+full_image[47:-29]

    ## Twitter Page
    browser.get('https://twitter.com/marswxreport?lang=en')
    elem1 = browser.find_element_by_name("session[username_or_email]")
    elem1.send_keys("MattGarber4")
    elem2 = browser.find_element_by_name("session[password]")
    elem2.send_keys("#Garb1122")
    elem3 = browser.find_element_by_class_name("EdgeButton")
    elem3.click()
    html = browser.page_source
    soup = bs(html,'html.parser')
    Paragraphs = soup.find_all('p')
    for paragraph in Paragraphs:
        if 'InSight sol' in paragraph.text:
            Mars_Weather = paragraph.text
            break

    # Pandas Scrape Table
    browser.get('https://space-facts.com/mars/')
    html2 = browser.page_source
    soup3 = bs(html2,'lxml')
    table= soup3.find_all('table')[0]
    df = pd.read_html(str(table))
    html_table = df[0].to_html()

    ## Hemispheric Images
    browser.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    elem4 = browser.find_elements_by_css_selector('img.thumb')
    image_list = []
    url = 'https://astrogeology.usgs.gov'
    for i in range(len(elem4)):
        image_dict = {}
        elem4[i].click()
        html3 = browser.page_source
        soup5 = bs(html3,'html.parser')
        image_dict['title'] = soup5.title.text[:-34]
        image_dict['img_url'] = soup5.find_all('img')[3]
        image_list.append(image_dict)

        browser.back()
        elem4 = browser.find_elements_by_css_selector('img.thumb')
    image_list

    scraped_data = {
                    'Mars_News_Title': Mars_News_Title,
                    'Mars_News_Text':Mars_News_Text,
                    'Nasa_Image':full_image_url,
                    'Mars_Weather': Mars_Weather,
                    'HTML_Table':html_table,
                    'Image1_Title':image_list[0]['title'],
                    'Image1_Url':url + image_list[0]['img_url']['src'],
                    'Image2_Title':image_list[1]['title'],
                    'Image2_Url':url +image_list[1]['img_url']['src'],
                    'Image3_Title':image_list[2]['title'],
                    'Image3_Url':url +image_list[2]['img_url']['src'],
                    'Image4_Title':image_list[3]['title'],
                    'Image4_Url':url +image_list[3]['img_url']['src'],

                                                    }
    return scraped_data   

    






