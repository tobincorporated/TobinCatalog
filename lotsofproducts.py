from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Product, User

engine = create_engine('sqlite:///productcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Zach Tobin", email="tobin.zachary@gmail.com",
             picture='https://lh3.googleusercontent.com/-Nrf8Py-fzI8/AAAAAAAAAAI/AAAAAAAAA2E/MzosFqeiD8I/photo.jpg')
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Category(user_id=1, name="Electronics")

session.add(category1)
session.commit()

product2 = Product(user_id=1, name="USB Cables", description="You need more USB cables. Buy them now.",
                     price="$3.50", category=category1)

session.add(product2)
session.commit()


product1 = Product(user_id=1, name="MotherBoard", description="You gotta build your own computer, man",
                     price="$200.99", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="LCD Monitor", description="A full 23in so you can see all the things in the pixels",
                     price="$125.50", category=category1)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Tablet Computer", description="So new, and with so many apps!",
                     price="$600.00", category=category1)

session.add(product3)
session.commit()

product4 = Product(user_id=1, name="Speakers", description="They bring the noise and the funk",
                     price="$70.99", category=category1)

session.add(product4)
session.commit()

product5 = Product(user_id=1, name="Optical Drive", description="I like DVDs",
                     price="$25.99", category=category1)

session.add(product5)
session.commit()

product6 = Product(user_id=1, name="Laptop", description="Coding on the go, right?",
                     price="$800.99", category=category1)

session.add(product6)
session.commit()



# Menu for Super Stir Fry
category2 = Category(user_id=1, name="Beverages")

session.add(category2)
session.commit()


product1 = Product(user_id=1, name="Root Beer", description="Pretty nice tasting.",
                     price="$1.99", category=category2)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Cola",
                     description="Too indecisive for a real flavor? Try this.", price="$1.99", category=category2)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Mojito", description="Zach\'s personal specialty",
                     price="$12.00", category=category2)

session.add(product3)
session.commit()

product4 = Product(user_id=1, name="Manhattan", description="For the old-fashioned who don\'t want an Old Fashioned.",
                     price="$12.00", category=category2)

session.add(product4)
session.commit()

product5 = Product(user_id=1, name="Whisky", description="Whisky is pretty nice.",
                     price="$12.00", category=category2)

session.add(product5)
session.commit()

# Menu for Panda Garden
category1 = Category(user_id=1, name="Martial Arts")

session.add(category1)
session.commit()


product1 = Product(user_id=1, name="Dogi", description="Look like a professional",
                     price="$28.99", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Sparring pads", description="It\'s fun to hit other people, now do it without the liability!",
                     price="$6.99", category=category1)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Katana", description="Slice bad guys and look cool doing it",
                     price="$399.95", category=category1)

session.add(product3)
session.commit()

# Menu for Thyme for that
category1 = Category(user_id=1, name="Tools")

session.add(category1)
session.commit()


product1 = Product(user_id=1, name="Hammer", description="It\'s a hammer",
                     price="$12.99", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Drill", description="More powerful than yours, so buy it.",
                     price="$45.99", category=category1)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Awl",
                    description="Poke holes with the best of them",
                    price="$4.50", category=category1)

session.add(product3)
session.commit()

product4 = Product(user_id=1, name="Utility knife", description="Don\'t cut yourself.",
                     price="$6.95", category=category1)

session.add(product4)
session.commit()

product5 = Product(user_id=1, name="Bottle Opener", description="For use with beverages",
                     price="$0.95", category=category1)

session.add(product5)
session.commit()


# Menu for Tony's Bistro
category1 = Category(user_id=1, name="Sewing")

session.add(category1)
session.commit()


product1 = Product(user_id=1, name="Needle", description="For use with thread",
                     price="$0.95", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Thread", description="For use with needle",
                     price="$4.95", category=category1)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Fabric", description="For use with needle and thread",
                     price="$6.95", category=category1)

session.add(product3)
session.commit()

product4 = Product(user_id=1, name="Scissors",
                     description="Cut fabric with these ultra shears", price="$3.95", category=category1)

session.add(product4)
session.commit()

# Menu for Auntie Ann's
category1 = Category(user_id=1, name="Food")

session.add(category1)
session.commit()

product9 = Product(user_id=1, name="Pizza",
                     description="Even if you\'re not in college anymore", price="$8.99", category=category1)

session.add(product9)
session.commit()


product1 = Product(user_id=1, name="Cookies", description="With chocolate chips",
                     price="$2.99", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Burger", description="With cheese and pickles and secret sauce",
                     price="$4.95", category=category1)

session.add(product2)
session.commit()

product3 = Product(user_id=1, name="Soup",
                     description="Eat when sick", price="$1.50", category=category1)

session.add(product3)
session.commit()

product4 = Product(user_id=1, name="Chicken", description="Pluck first",
                     price="$8.95", category=category1)

session.add(product4)
session.commit()


# Menu for Cocina Y Amor
category1 = Category(user_id=1, name="Office Supplies")

session.add(category1)
session.commit()


product1 = Product(user_id=1, name="Pencil",
                     description="Mechanical pencils are great.", price="$5.95", category=category1)

session.add(product1)
session.commit()

product2 = Product(user_id=1, name="Pen", description="Pack of 100 because pens are awful. ",
                     price="$7.99", category=category1)

session.add(product2)
session.commit()

product1 = Product(user_id=1, name="Printer Paper", 
                    description="Print or scribble on this stuff.",
                    price="$5.95",
                    category=category1)

session.add(product1)
session.commit()

product1 = Product(user_id=1, name="Tape",
                     description="Now you can hold any two things together indefinitely", price="$6.95", category=category1)

session.add(product1)
session.commit()


product1 = Product(user_id=1, name="Stapler",
                     description="Better than tape", price="$8.25",  category=category1)

session.add(product1)
session.commit()


print "added products!"
