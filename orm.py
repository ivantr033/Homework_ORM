## 1 задание.

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='publisher')

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    stock = relationship('Stock', back_populates='book')

class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    stock = relationship('Stock', back_populates='shop')

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship('Book', back_populates='stock')
    shop = relationship('Shop', back_populates='stock')
    sales = relationship('Sale', back_populates='stock')

class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=True)

    stock = relationship('Stock', back_populates='sales')


## 2 задание.

import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, Base

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'test_db')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)

def load_test_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    with open('fixtures/tests_data.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    session.close()
    print("Тестовые данные успешно загружены.")

def find_purchases_by_publisher(publisher_input):
    """
    Выводит покупки книг заданного издателя.
    :param publisher_input: Имя издателя (строка) или его идентификатор (число)
    """
    with Session() as session:
        # Преобразуем ввод в число или строку
        if publisher_input.isdigit():
            publisher_input = int(publisher_input)
            publisher_filter = Publisher.id == publisher_input
        else:
            publisher_filter = Publisher.name == publisher_input

        # Поиск издателя
        publisher = session.query(Publisher).filter(publisher_filter).one_or_none()

        if not publisher:
            print(f"Издатель '{publisher_input}' не найден.")
            return

        # Запрос данных о покупках
        purchases_query = (
            session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
            .join(Stock, Stock.id_book == Book.id)
            .join(Sale, Sale.id_stock == Stock.id)
            .join(Shop, Stock.id_shop == Shop.id)
            .filter(Book.id_publisher == publisher.id)
            .order_by(Sale.date_sale)
        )

        print(f"Покупки книг издателя '{publisher.name}':")
        for title, shop_name, price, date_sale in purchases_query:
            print(f"{title} | {shop_name:15} | {price} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == "__main__":
    print("1. Загрузить тестовые данные")
    print("2. Найти покупки по издателю")
    choice = input("Выберите действие (1 или 2): ").strip()

    if choice == "1":
        load_test_data()
    elif choice == "2":
        publisher_input = input("Введите имя или идентификатор издателя: ").strip()
        find_purchases_by_publisher(publisher_input)
    else:
        print("Неверный выбор. Завершение программы.")


## 3 задание (необязательное).
"""
[
    {
        "model": "publisher",
        "pk": 1,
        "fields": {
            "name": "Эксмо"
        }
    },
    {
        "model": "publisher",
        "pk": 2,
        "fields": {
            "name": "АСТ"
        }
    },
    {
        "model": "publisher",
        "pk": 3,
        "fields": {
            "name": "Питер"
        }
    },
    {
        "model": "publisher",
        "pk": 4,
        "fields": {
            "name": "Миф"
        }
    },
    {
        "model": "book",
        "pk": 1,
        "fields": {
            "title": "Мастер и Маргарита",
            "id_publisher": 1
        }
    },
    {
        "model": "book",
        "pk": 2,
        "fields": {
            "title": "Преступление и наказание",
            "id_publisher": 2
        }
    },
    {
        "model": "book",
        "pk": 3,
        "fields": {
            "title": "Война и мир",
            "id_publisher": 2
        }
    },
    {
        "model": "book",
        "pk": 4,
        "fields": {
            "title": "Анна Каренина",
            "id_publisher": 1
        }
    },
    {
        "model": "book",
        "pk": 5,
        "fields": {
            "title": "Братья Карамазовы",
            "id_publisher": 2
        }
    },
    {
        "model": "book",
        "pk": 6,
        "fields": {
            "title": "Чистый код",
            "id_publisher": 3
        }
    },
    {
        "model": "book",
        "pk": 7,
        "fields": {
            "title": "Совершенный программист",
            "id_publisher": 3
        }
    },
    {
        "model": "book",
        "pk": 8,
        "fields": {
            "title": "Алгоритмы. Построение и анализ",
            "id_publisher": 3
        }
    },
    {
        "model": "book",
        "pk": 9,
        "fields": {
            "title": "Java. Руководство для начинающих",
            "id_publisher": 3
        }
    },
    {
        "model": "book",
        "pk": 10,
        "fields": {
            "title": "Программирование на Python",
            "id_publisher": 3
        }
    },
    {
        "model": "book",
        "pk": 16,
        "fields": {
            "title": "Чистый код",
            "id_publisher": 3
        }
    },
    {
        "model": "stock",
        "pk": 6,
        "fields": {
            "id_book": 16,
            "id_shop": 1,
            "count": 20
        }
    },
    {
        "model": "sale",
        "pk": 6,
        "fields": {
            "price": 700,
            "date_sale": "2024-12-01",
            "id_stock": 6,
            "count": 5
        }
    },

    {
        "model": "book",
        "pk": 11,
        "fields": {
            "title": "1Q84",
            "id_publisher": 4
        }
    },
    {
        "model": "book",
        "pk": 12,
        "fields": {
            "title": "Норвежский лес",
            "id_publisher": 4
        }
    },
    {
        "model": "book",
        "pk": 13,
        "fields": {
            "title": "Маленький принц",
            "id_publisher": 4
        }
    },
    {
        "model": "book",
        "pk": 14,
        "fields": {
            "title": "Гарри Поттер и философский камень",
            "id_publisher": 4
        }
    },
    {
        "model": "book",
        "pk": 15,
        "fields": {
            "title": "Гарри Поттер и тайная комната",
            "id_publisher": 4
        }
    },
    {
        "model": "shop",
        "pk": 1,
        "fields": {
            "name": "Буквоед"
        }
    },
    {
        "model": "shop",
        "pk": 2,
        "fields": {
            "name": "Лабиринт"
        }
    },
    {
        "model": "shop",
        "pk": 3,
        "fields": {
            "name": "Читай-город"
        }
    },
    {
        "model": "shop",
        "pk": 4,
        "fields": {
            "name": "ЛитРес"
        }
    },
    {
        "model": "stock",
        "pk": 1,
        "fields": {
            "id_book": 1,
            "id_shop": 1,
            "count": 10
        }
    },
    {
        "model": "stock",
        "pk": 2,
        "fields": {
            "id_book": 2,
            "id_shop": 2,
            "count": 5
        }
    },
    {
        "model": "stock",
        "pk": 3,
        "fields": {
            "id_book": 3,
            "id_shop": 3,
            "count": 7
        }
    },
    {
        "model": "stock",
        "pk": 4,
        "fields": {
            "id_book": 4,
            "id_shop": 4,
            "count": 15
        }
    },
    {
        "model": "stock",
        "pk": 5,
        "fields": {
            "id_book": 5,
            "id_shop": 1,
            "count": 8
        }
    },
    {
        "model": "sale",
        "pk": 1,
        "fields": {
            "price": 500,
            "date_sale": "2024-11-25",
            "id_stock": 1,
            "count": 3
        }
    },
    {
        "model": "sale",
        "pk": 2,
        "fields": {
            "price": 450,
            "date_sale": "2024-11-26",
            "id_stock": 2,
            "count": 2
        }
    },
    {
        "model": "sale",
        "pk": 3,
        "fields": {
            "price": 600,
            "date_sale": "2024-11-27",
            "id_stock": 3,
            "count": 1
        }
    },
    {
        "model": "sale",
        "pk": 4,
        "fields": {
            "price": 700,
            "date_sale": "2024-11-28",
            "id_stock": 4,
            "count": 4
        }
    },
    {
        "model": "sale",
        "pk": 5,
        "fields": {
            "price": 550,
            "date_sale": "2024-11-29",
            "id_stock": 5,
            "count": 2
        }
    }
]
"""