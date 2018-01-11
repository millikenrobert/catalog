from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, SportsItem, User

engine = create_engine('sqlite:///catalog.db')
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
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Soccer Ball", description="A round ball, black and white", category=category1)

session.add(menuItem2)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Goal post", description="kick the ball through these", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="knee pads", description="Protect your knees", category=category1)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Minivan", description="Get to soccer safely", category=category1)

session.add(menuItem3)
session.commit()

menuItem4 = SportsItem(user_id=1, name="Mouth guard", description="Protect your teeth", category=category1)

session.add(menuItem4)
session.commit()

menuItem5 = SportsItem(user_id=1, name="Beer", description="Make soccer tolerable", category=category1)

session.add(menuItem5)
session.commit()

menuItem6 = SportsItem(user_id=1, name="Iced Tea", description="Through this over soccer kids", category=category1)

session.add(menuItem6)
session.commit()

menuItem7 = SportsItem(user_id=1, name="Energy Bar",
                       description="Eat this", category=category1)

session.add(menuItem7)
session.commit()

menuItem8 = SportsItem(user_id=1, name="Grass", description="Play soccer on grass", category=category1)

session.add(menuItem8)
session.commit()


# Menu for Super Stir Fry
category2 = Category(user_id=1, name="Diving")

session.add(category2)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Regulator", description="Attach to mouth, breath", category=category2)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Mask",
                       description="Enables the users to see under water", category=category2)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Snorkel", description="Breathe through this ", category=category2)

session.add(menuItem3)
session.commit()

menuItem4 = SportsItem(user_id=1, name="Fins", description="Swim with these on your feet ", category=category2)

session.add(menuItem4)
session.commit()

menuItem5 = SportsItem(user_id=1, name="Tank", description="Put air in it foor breathing.", category=category2)

session.add(menuItem5)
session.commit()

menuItem6 = SportsItem(user_id=1, name="Wetsuit", description="Stay warm under water", category=category2)

session.add(menuItem6)
session.commit()


# Menu for Panda Garden
category1 = Category(user_id=1, name="Skating")

session.add(category1)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Converse Sneakers", description="Put on your feet.", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Skateboard", description="Skate with this", category=category1)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Rollerblades", description="An embarrasing pastime", category=category1)

session.add(menuItem3)
session.commit()

menuItem4 = SportsItem(user_id=1, name="Hocky Stick", description="Hit people with this", category=category1)

session.add(menuItem4)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Wheels", description="Replace your wheels", category=category1)

session.add(menuItem2)
session.commit()


# Menu for Thyme for that
category1 = Category(user_id=1, name="Waterskiing")

session.add(category1)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Boat", description="Some to tow you with", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Skis", description="Put on feet", category=category1)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Bathers",
                       description="Not able to wear jeans", category=category1)

session.add(menuItem3)
session.commit()

menuItem4 = SportsItem(user_id=1, name="Helmet", description="Put on head", category=category1)

session.add(menuItem4)
session.commit()

menuItem5 = SportsItem(user_id=1, name="Rope", description="Get dragged behind a boat", category=category1)

session.add(menuItem5)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Water", description="Required for water skiing", category=category1)

session.add(menuItem2)
session.commit()


# Menu for Tony's Bistro
category1 = Category(user_id=1, name="Frisbee ")

session.add(category1)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Frisbee", description="Throw this", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Knitted beanie", description="Frisbee haute couture", category=category1)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Dark glasses", description="Hide those bloodshot eyes", category=category1)

session.add(menuItem3)
session.commit()


# Menu for Andala's
category1 = Category(user_id=1, name="Basketball")

session.add(category1)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Ball", description="Throw and bounce the ball", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Hoop", description="Throw ball through hoop", category=category1)

session.add(menuItem2)
session.commit()

menuItem3 = SportsItem(user_id=1, name="Shoes", description="Put on feet.", category=category1)

session.add(menuItem3)
session.commit()

menuItem4 = SportsItem(user_id=1, name="Referee", description="This person tells you what to do", category=category1)

session.add(menuItem4)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Siren", description="Listen and-or ring the bell", category=category1)

session.add(menuItem2)
session.commit()


# Menu for Auntie Ann's
category1 = Category(user_id=1, name="Rock climbing")

session.add(category1)
session.commit()

menuItem9 = SportsItem(user_id=1, name="Rocks",
                       description="Climb on these", category=category1)

session.add(menuItem9)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Cliff", description="Climb up this", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Roap", description="Attach this to an anchor point", category=category1)

session.add(menuItem2)
session.commit()


# Menu for Cocina Y Amor
category1 = Category(user_id=1, name="Bug collecting")

session.add(category1)
session.commit()


menuItem1 = SportsItem(user_id=1, name="Trap",
                       description="Trap a bug", category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = SportsItem(user_id=1, name="Pins", description="Pin them to a board, best pins here", category=category1)

session.add(menuItem2)
session.commit()


menuItem3 = SportsItem(user_id=1, name="Boots", description="Dont get bitten by snakes by wearing these boots", category=category1)

session.add(menuItem3)
session.commit

menuItem4 = SportsItem(user_id=1, name="Net",
                       description="Needed to catch flying bugs", category=category1)

session.add(menuItem4)
session.commit()
