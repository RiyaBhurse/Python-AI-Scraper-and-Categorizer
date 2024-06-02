
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the Post class
class Post(Base):
    __tablename__ = 'posts'
    url = Column(String, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    created_time = Column(DateTime)
    category = Column(String)
    
engine = create_engine('sqlite:///reddit_posts.db')
Base.metadata.create_all(engine)
