import praw
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(
    client_id='SduFPk6KdVwYy2VGCPdDtQ',
    client_secret='GgLB6T9zLJyR33OJGlcGHXB7Fj-9Jg',
    user_agent='RedScrape'
)

# Set up the database with SQLAlchemy
Base = declarative_base()
import praw
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Reddit API credentials
reddit = praw.Reddit(
    client_id='SduFPk6KdVwYy2VGCPdDtQ',
    client_secret='GgLB6T9zLJyR33OJGlcGHXB7Fj-9Jg',
    user_agent='RedScrape'
)

# Set up the database with SQLAlchemy
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    url = Column(String, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    created_time = Column(DateTime)
    category = Column(String)  # Add a category column

engine = create_engine('sqlite:///reddit_posts.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Example training data
texts = ["I love programming.", "I hate bugs.", "Python is great!", "I dislike syntax errors."]
labels = ["positive", "negative", "positive", "negative"]

# Create a model pipeline
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(texts, labels)

def classify_text(text):
    processed_text = preprocess_text(text)
    return model.predict([processed_text])[0]

def scrape_and_store():
    subreddit = reddit.subreddit('all')
    latest_posts = subreddit.new(limit=1000)
    
    for post in latest_posts:
        title = post.title.strip()
        content = post.selftext.strip() if post.is_self else "[Non-text post]"
        url = post.url
        created_time = datetime.fromtimestamp(post.created_utc)
        category = classify_text(content)

        if not session.query(Post).filter_by(url=url).first():
            new_post = Post(url=url, title=title, content=content, created_time=created_time, category=category)
            session.add(new_post)
            session.commit()

try:
    while True:
        scrape_and_store()
        print("Scraped, classified, and stored data.")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    session.close()

class Post(Base):
    __tablename__ = 'posts'
    url = Column(String, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    created_time = Column(DateTime)  # Add the created_time column

engine = create_engine('sqlite:///reddit_posts.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_and_store():
    # Get the latest posts from a subreddit
    subreddit = reddit.subreddit('all')
    latest_posts = subreddit.new(limit=1000)
    
    # Insert the details of the latest posts into the database
    for post in latest_posts:
        title = post.title.strip()
        content = post.selftext.strip() if post.is_self else "[Non-text post]"
        url = post.url  # Extract the URL
        created_time = datetime.fromtimestamp(post.created_utc)  # Extract the post creation time

        # Check if the post is already in the database to avoid duplicates
        if not session.query(Post).filter_by(url=url).first():
            new_post = Post(url=url, title=title, content=content, created_time=created_time)
            session.add(new_post)
            session.commit()

try:
    while True: 
        scrape_and_store()
        print("Scraped and stored data.")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Close the session
    session.close()
