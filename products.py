import json

from controllers.product import product_process_quantity
from models.category import Category
from models.product import Product
from utils import SessionLocal

db = SessionLocal()


def create_category(title: str, parent=None):
    category = db.query(Category).filter_by(title=title.strip()).first()
    if not category:
        category = Category(title=title.strip(), parent_id=parent.id if parent else None)
        db.add(category)
        db.commit()
    return category


# def process_quantity(miktar):
#     if not miktar or miktar == '0.000':
#         return 0
#
#     try:
#         return int(miktar.replace(',', ''))
#     except ValueError:
#         return 0


def save_data(data):
    for item in data:
        kategori_a = create_category(item['KategoriA'])
        kategori_b = create_category(item['KategoriB'], parent=kategori_a)
        kategori_c = create_category(item['KategoriC'], parent=kategori_b)

        product = Product(
            title=item['TanimRU'].strip(),
            description=None,
            price=None,
            image_path=None,
            # quantity=process_quantity(item['Miktar']),
            quantity=product_process_quantity(item['quantity']),
            article=item['Artikel'].strip(),
            code=item['Kod'].strip(),
            unit=item['Birim'].strip(),
            category_id=kategori_c.id,
        )
        db.add(product)

    db.commit()


if __name__ == '__main__':
    with open('./data.json', 'r', encoding='utf-8') as file:
        data_ = json.load(file)
    print(f"Загружено {len(data_)} продуктов.")
    save_data(data_)

    db.close()
