import requests
from bs4 import BeautifulSoup
import json


scraped_books = []

HOST_NAME = 'http://books.toscrape.com/catalogue/'

page_number = 1
while True:
    url = HOST_NAME + 'page-{}.html'.format(page_number)
    response = requests.get(url)
    if response.status_code == 404:
        break
    soup = BeautifulSoup(response.content, "lxml", from_encoding='utf-8')
    books = soup.find_all('article', {'class': 'product_pod'})
    for book in books:
        rating = book.find('p')['class'][1]
        book_link = book.find('h3').find('a')['href']
        title = book.find('h3').find('a')['title']
        price = book.find('p', {'class': 'price_color'}).text
        book_page = HOST_NAME + book_link
        response = requests.get(book_page)
        soup = BeautifulSoup(response.content, "lxml", from_encoding='utf-8')
        category = soup.find('ul').find_all('li')[2].text.strip()
        try:
            description = soup.find(id='product_description').find_next('p').text.replace('"', '\'')
        except AttributeError:
            description = ''
        scraped_books.append({'title': title,
                              'rating': rating,
                              'price': price,
                              'description': description,
                              'category': category})
    page_number += 1

with open('books.json', 'w') as outfile:
    json.dump({'books': scraped_books}, outfile, ensure_ascii=False, indent=4)

