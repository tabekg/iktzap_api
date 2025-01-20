import json

from flask import g

from main import app
from models.category import Category
from models.product import Product
from utils import SessionLocal

db = SessionLocal()


def create_category(title, parent=None):
    category = db.query(Category).filter_by(title=title).first()
    if not category:
        category = Category(title=title, parent_id=parent.id if parent else None)
        db.add(category)
        db.commit()
    return category


def process_quantity(miktar):
    if not miktar or miktar == '0.000':
        return 0

    try:
        return int(miktar.replace(',', ''))
    except ValueError:
        return 0


def save_data(data):
    for item in data:
        kategori_a = create_category(item['KategoriA'])
        kategori_b = create_category(item['KategoriB'], parent=kategori_a)
        kategori_c = (create_category(item['KategoriC'], parent=kategori_b))

        product = Product(
            title=item['TanimRU'],
            description=None,
            price=None,
            image_path=None,
            quantity=process_quantity(item['Miktar']),
            article=item['Artikel'],
            code=item['Kod'],
            unit=item['Birim'],
            category_id=kategori_a.id
        )
        db.add(product)

    db.commit()


if __name__ == '__main__':
    with app.app_context():
        with open('C:/Users/HP/Desktop/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Загружено {len(data)} продуктов.")
        save_data(data)

