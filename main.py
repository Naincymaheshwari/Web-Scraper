from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
from datetime import datetime

URL = "https://www.theverge.com"


def initiallise_driver():
    return webdriver.Chrome(r"C:\Users\nainc\OneDrive\Desktop\Projects\web scrapper\chromedriver.exe")


def crawl_data(driver):
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    articles = soup.find_all('div', class_='duet--content-cards--content-card')
    return find_data(articles)
   

def find_data(articles):
    article_id = 0
    content = []
    for article in articles:
        article_title = ""
        article_author = ""
        article_publish_date = ""
        article_url = ""
        title_obj = article.find('h2')
        if title_obj is not None:
            article_title = title_obj.find('a').text.strip()
            article_url = URL + title_obj.find('a')['href'].strip()
            if article_title != "":
                article_id += 1

        author_obj = article.find('div', {"class": "relative z-10 inline-block pt-4 font-polysans text-11 uppercase leading-140 tracking-15 text-gray-31 dark:text-gray-bd"})
        if author_obj is not None:
            article_author = author_obj.find('a').text.strip()
            article_publish_date = author_obj.find('span').text.strip()
        if article_title != "":
            obj = {
                "id": article_id,
                "url": article_url,
                "headline": article_title,
                "author": article_author,
                "date": article_publish_date
            }
            content.append(obj)
        
    return content


def save_content_to_file(results):
    file_name = datetime.now().strftime("%d%m%Y")
    data_file = open(str(file_name)+"_verge.csv", 'w')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(results[0])
    for obj in results:
       csv_writer.writerow(obj.values())
 
    data_file.close()


if __name__ == "__main__":
    driver = initiallise_driver()
    result = crawl_data(driver)
    save_content_to_file(result)
