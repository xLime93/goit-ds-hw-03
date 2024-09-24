from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://username:password@cluster0.uyk3q.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.ds_hw3_2

# Читання (Read)
# Реалізуйте функцію для виведення всіх записів із колекції.
def print_all_items():
    result = db.cats.find({})
    for el in result:
        print(el)

print_all_items()

# Реалізуйте функцію, яка дозволяє користувачеві ввести ім'я кота та виводить інформацію про цього кота.
def search_cat():
    cat_name = input('Введіть імʼя кота для пошуку: ')
    result = db.cats.find_one({"name": cat_name})
    print(result)

search_cat()

# Оновлення (Update)
# Створіть функцію, яка дозволяє користувачеві оновити вік кота за ім'ям.
def update_one():
    cat_name = input('Введіть імʼя кота для оновлення віку: ')
    cat_age = int(input('Введіть вік кота: '))
    db.cats.update_one({"name": cat_name}, {"$set": {"age": cat_age}})
    result = db.cats.find_one({"name": cat_name})
    print(result)

update_one()

# Створіть функцію, яка дозволяє додати нову характеристику до списку features кота за ім'ям.
def add_features():
    cat_name = input('Введіть імʼя кота для додавання нової характеристики: ')
    cat_features = input('Введіть нову характеристику кота: ')
    db.cats.update_one({"name": cat_name}, {"$push": {"features": cat_features}})
    result = db.cats.find_one({"name": cat_name})
    print(result)

add_features()

# Видалення (Delete)
# Реалізуйте функцію для видалення запису з колекції за ім'ям тварини.
def del_cat():
    cat_name = input('Введіть імʼя кота для видалення: ')
    db.cats.delete_one({"name": cat_name})
    result = db.cats.find_one({"name": cat_name})
    print(result)

del_cat()

# Реалізуйте функцію для видалення всіх записів із колекції.
def delete_all():
    confirm = input('Бажаєте видалити всіх котів? y/n ')
    if confirm == 'y':
        db.cats.delete_many({})
        print('Котів видалено')
    else:
        print('Котів не видалено')

delete_all()