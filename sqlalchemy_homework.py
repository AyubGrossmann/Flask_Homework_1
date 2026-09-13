from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


# SQLite database in memory
engine = create_engine("sqlite:///:memory:")


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


print("SQLite engine created successfully")
print("Session created successfully")
print("Product and Category models created successfully")
print("Relationship between Product and Category created successfully")