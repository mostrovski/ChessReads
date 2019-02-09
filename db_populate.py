from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Book

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create dummy user
firstUser = User(name='Chess Lover',
                 email='tinnyTim@udacity.com',
                 picture='http://bit.ly/2DdqbNl')
session.add(firstUser)
session.commit()
'''
Create category 'Improvement'
'''
category1 = Category(name='Improvement', user=firstUser)
session.add(category1)
session.commit()
# Add book 'My System'
description = 'My System is at the top of a very short list of chess classics'
mySystem = Book(title='My System',
                author='Aron Nimzowitsch',
                description=description,
                category=category1,
                user=firstUser)
session.add(mySystem)
session.commit()
# Add book 'Under the Surface'
description = '''This book invites you beneath the surface, where you can 
learn to navigate the depths of chess'''
underTheSurface = Book(title='Under the Surface',
                       author='Jan Markos',
                       description=description,
                       category=category1,
                       user=firstUser)
session.add(underTheSurface)
session.commit()
# Add book 'Understanding Chess Move by Move'
description = 'Moves are explained using words that everyone can understand'
understandingChess = Book(title='Understanding Chess Move by Move',
                          author='John Nunn',
                          description=description,
                          category=category1,
                          user=firstUser)
session.add(understandingChess)
session.commit()
'''
Create category 'Openings'
'''
category2 = Category(name='Openings', user=firstUser)
session.add(category2)
session.commit()
# Add book 'My First Chess Opening Repertoire for White'
description = 'A turn-key package for ambitious beginners'
repertoireWhite = Book(title='My First Chess Opening Repertoire for White',
                       author='Vincent Moret',
                       description=description,
                       category=category2,
                       user=firstUser)
session.add(repertoireWhite)
session.commit()
# Add book 'My First Chess Opening Repertoire for Black'
description = 'A ready-to-go package for ambitious beginners'
repertoireBlack = Book(title='My First Chess Opening Repertoire for Black',
                       author='Vincent Moret',
                       description=description,
                       category=category2,
                       user=firstUser)
session.add(repertoireBlack)
session.commit()
'''
Create category 'Middlegames'
'''
category3 = Category(name='Middlegames', user=firstUser)
session.add(category3)
session.commit()
# Add book 'Understanding Chess Middlegames'
description = '''The three-times World Chess Solving Champion distils the most 
useful middlegame concepts and knowledge into 100 lessons that everyone can 
understand'''
chessMiddlegames = Book(title='Understanding Chess Middlegames',
                        author='John Nunn', 
                        description=description,
                        category=category3,
                        user=firstUser)
session.add(chessMiddlegames)
session.commit()
'''
Create category 'Endgames'
'''
category4 = Category(name='Endgames', user=firstUser)
session.add(category4)
session.commit()
# Add book 'Understanding Chess Endgames'
description = '''One of the best chess writers provides everything you need to 
know about chess endgames'''
chessEndgames = Book(title='Understanding Chess Endgames',
                     author='John Nunn',
                     description=description,
                     category=category4,
                     user=firstUser)
session.add(chessEndgames)
session.commit()
'''
Create category 'Tactics'
'''
category5 = Category(name='Tactics', user=firstUser)
session.add(category5)
session.commit()
# Add book 'Chess Tactics from Scratch'
description = '''This expanded second edition offers more puzzles to test the 
tactical chess skill that the author helps the reader develop'''
chessTactics = Book(title='Chess Tactics from Scratch',
                    author='Martin Weteschnik',
                    description=description,
                    category=category5,
                    user=firstUser)
session.add(chessTactics)
session.commit()
'''
Create category 'Strategy'
'''
category6 = Category(name='Strategy', user=firstUser)
session.add(category6)
session.commit()
# Add book 'Chess Strategy for Club Players'
description = '''Every club player knows the problem: the opening has ended, 
and now what? First find the right plan, then the good moves will follow'''
chessStrategy = Book(title='Chess Strategy for Club Players',
                     author='Herman Grooten',
                     description=description,
                     category=category6,
                     user=firstUser)
session.add(chessStrategy)
session.commit()
'''
Create category 'Stories'
'''
category7 = Category(name='Stories', user=firstUser)
session.add(category7)
session.commit()
# Add book 'The World Champions I Knew'
description = '''An important addition to what we know about the lives of the 
world champions. This is chess literature at its very best'''
worldChampions = Book(title='The World Champions I Knew',
                      author='Genna Sosonko',
                      description=description,
                      category=category7,
                      user=firstUser)
session.add(worldChampions)
session.commit()

print('added books!')
