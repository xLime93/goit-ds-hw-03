import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://username:password@cluster0.uyk3q.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.ds_hw3_2

base_url = "http://quotes.toscrape.com"
quotes_data = []
authors_data = []
visited_authors = set()

def get_quotes_and_authors(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # скрапаємо цитати
    for quote_block in soup.find_all('div', class_='quote'):
        quote_text = quote_block.find('span', class_='text').get_text()
        author_name = quote_block.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote_block.find_all('a', class_='tag')]

        # додавання інформації з цитатами
        quotes_data.append({
            'tags': tags,
            'author': author_name,
            'quote': quote_text
        })
        
        # скрапаємо деталі про авторів
        if author_name not in visited_authors:
            author_link = quote_block.find('a')['href']
            get_author_details(base_url + author_link)
            visited_authors.add(author_name)

    # перевірка наявності наступної сторінки
    next_page = soup.find('li', class_='next')
    if next_page:
        next_link = next_page.find('a')['href']
        get_quotes_and_authors(base_url + next_link)

def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    fullname = soup.find('h3', class_='author-title').get_text().strip()
    born_date = soup.find('span', class_='author-born-date').get_text().strip()
    born_location = soup.find('span', class_='author-born-location').get_text().strip()
    description = soup.find('div', class_='author-description').get_text().strip()
    
    # додаємо інформацію про авторів
    authors_data.append({
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    })

# початок скрапінгу
get_quotes_and_authors(base_url)

# збереження даних з цитатами
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

# збереження даних з автоами
with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_data, f, ensure_ascii=False, indent=4)

# збереження інформації до бази даних монго
result_many = db.quotes.insert_many(quotes_data)
result_many = db.authors.insert_many(authors_data)


# def delete_all():
#     db.quotes.delete_many({})
#     db.authors.delete_many({})

# delete_all()