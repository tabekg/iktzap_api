from models.category import Category
from models.product import Product


def create_category(db, title: str, parent=None):
    category = db.query(Category).filter_by(title=title.strip()).first()
    if not category:
        category = Category(title=title.strip(), parent_id=parent.id if parent else None)
        db.add(category)
        db.commit()
    return category


def product_process_quantity(q):
    return {
        'chita': q.get('chita', 0),
        'kultuma': q.get('kultuma', 0),
        'ozerny': q.get('ozerny', 0),
    }


def import_json(db, data):
    for item in data:
        kategori_a = create_category(db, item['KategoriA'])
        kategori_b = create_category(db, item['KategoriB'], parent=kategori_a)
        kategori_c = create_category(db, item['KategoriC'], parent=kategori_b)

        product = db.query(Product).filter(Product.article == item['Artikel'].strip()).first()

        if product:
            product.title = item['TanimRU'].strip()
            product.description = item['description']
            product.price = item['price']
            product.quantity = product_process_quantity(item['quantity'])
            product.code = item['Kod'].strip()
            product.unit = item['Birim'].strip()
            product.category_id = kategori_c.id
        else:
            product = Product(
                title=item['TanimRU'].strip(),
                description=item['description'],
                price=item['price'],
                image_path=None,
                quantity=product_process_quantity(item['quantity']),
                article=item['Artikel'].strip(),
                code=item['Kod'].strip(),
                unit=item['Birim'].strip(),
                category_id=kategori_c.id,
            )
            db.add(product)
