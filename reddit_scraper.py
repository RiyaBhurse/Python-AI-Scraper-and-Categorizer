import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Post  # Import from database.py
from nlp import preprocess_text, classify_text  # Import from nlp.py
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(
    client_id='SduFPk6KdVwYy2VGCPdDtQ',
    client_secret='GgLB6T9zLJyR33OJGlcGHXB7Fj-9Jg',
    user_agent='RedScrape'
)

# Set up the database
engine = create_engine('sqlite:///reddit_posts.db')
Session = sessionmaker(bind=engine)
session = Session()

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
