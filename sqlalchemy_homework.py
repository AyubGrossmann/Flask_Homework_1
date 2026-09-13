from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import func
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


# SQLite database in memory
engine = create_engine("sqlite:///sqlalchemy_homework.db")
# engine = create_engine("sqlite:///:memory:")



# Session
Session = sessionmaker(bind=engine)
session = Session()


# Base class
class Base(DeclarativeBase):
    pass


# Category model
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )


# Product model
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    price: Mapped[float] = mapped_column(Numeric(10, 2))

    in_stock: Mapped[bool] = mapped_column(Boolean)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    category: Mapped["Category"] = relationship(
        back_populates="products"
    )


# Create tables
Base.metadata.create_all(engine)


with Session() as session:
    # Задание 1: добавление категорий
    electronics = Category(name="Электроника", description="Гаджеты и устройства")
    books = Category(name="Книги", description="Печатные книги и электронные книги")
    clothes = Category(name="Одежда", description="Одежда для мужчин и женщин")

    session.add_all([electronics, books, clothes])
    session.commit()

    # Задание 1: добавление продуктов
    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=electronics),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books),
        Product(name="Джинсы", price=40.50, in_stock=True, category=clothes),
        Product(name="Футболка", price=20.00, in_stock=True, category=clothes),
    ]

    session.add_all(products)
    session.commit()

    print("Данные успешно добавлены!")


# Очистка старых данных
session.query(Product).delete()
session.query(Category).delete()
session.commit()

# Add categories
electronics = Category(
    name="Электроника",
    description="Гаджеты и устройства"
)

books = Category(
    name="Книги",
    description="Печатные книги и электронные книги"
)

clothes = Category(
    name="Одежда",
    description="Одежда для мужчин и женщин"
)




# Add products
products = [
    Product(
        name="Смартфон",
        price=299.99,
        in_stock=True,
        category=electronics
    ),
    Product(
        name="Ноутбук",
        price=499.99,
        in_stock=True,
        category=electronics
    ),
    Product(
        name="Научно-популярный роман",
        price=15.99,
        in_stock=True,
        category=books
    ),
    Product(
        name="Джинсы",
        price=40.50,
        in_stock=True,
        category=clothes
    ),
    Product(
        name="Футболка",
        price=20.00,
        in_stock=True,
        category=clothes
    )
]

session.add_all([electronics, books, clothes])
session.commit()

# Задание 2: чтение данных

categories = session.query(Category).all()

for category in categories:
    print(f"\nКатегория: {category.name}")
    for product in category.products:
            print(f"  {product.name} — {product.price}")

# Задание 3: обновление данных
product = session.query(Product).filter_by(name="Смартфон").first()

if product:
    product.price = 349.99
    session.commit()
    print(f"Цена смартфона обновлена: {product.price}")

session.add_all(products)
session.commit()

# Задание 4: Агрегация и группировка

result = (
    session.query(Category.name, func.count(Product.id))
    .outerjoin(Product, Category.id == Product.category_id)
    .group_by(Category.id, Category.name)
    .all()
)

for category_name, product_count in result:
    print(f"Категория: {category_name}, Количество товаров: {product_count}")


# Задание 5: Группировка с фильтрацией

result = (
    session.query(Category.name, func.count(Product.id))
    .outerjoin(Product, Category.id == Product.category_id)
    .group_by(Category.id, Category.name)
    .having(func.count(Product.id) > 1)
    .all()
)

for category_name, product_count in result:
    print(f"Категория: {category_name}, Количество товаров: {product_count}")




print("Categories and products added successfully")
print("SQLite engine created successfully")
print("Session created successfully")
print("Product and Category models created successfully")
print("Relationship between Product and Category created successfully")
print("Relationship between Product and Category created successfully")