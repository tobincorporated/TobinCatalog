from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """
    User class. Stores user information.

    Attributes:
        id: ID number of user
        name: user's name
        email: user's e-mail address
        picture: URL of user's profile picture
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    """
    Category class. Stores information on product category.

    Attributes:
        id: ID number of category
        name: category's name
        user_id: ID of the user who created the category
        user: relationship to User class
    """

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {'name': self.name,
                'id': self.id,
                }


class Product(Base):
    """
    Product class. Stores information on product.

    Attributes:
        id: ID number of product
        name: product's name
        description: description of product
        category_id: ID of category the product belongs to
        category: relationship to User class
        user_id: ID of the user that created the product
        user: relationship to User class
    """

    __tablename__ = 'product'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category,
                            backref=backref('product', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {'name': self.name,
                'description': self.description,
                'id': self.id,
                'price': self.price,
                }


engine = create_engine('sqlite:///productcatalog.db')

Base.metadata.create_all(engine)
