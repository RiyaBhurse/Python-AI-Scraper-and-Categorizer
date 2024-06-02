import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pandas as pd

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
texts = [
    "I struggle with coding interviews.", 
    "Learning new programming languages is challenging.",
    "As a software engineer, I want to upskill.",
    "Students need better resources for learning tech skills.",
    "The latest tech trends are exciting.",
    "I enjoy solving algorithmic problems.",
    "The tech industry is constantly evolving.",
    "Healthcare advancements are crucial.",
    "Global warming concerns me.",
    "Recycling can save the planet.",
    "Pollution is a serious issue.",
    "How to become a data scientist?",
    "How to learn web development?",
    "How to become a machine learning engineer?",
    "How to learn cloud computing?",
    "I want to learn data science.",
    "I want to learn web development.",
    "I want to learn machine learning.", 
    "I want to learn programming.",
    "I want to dance",
    "I want to sing",
    # Add around 50 more examples here
]

labels = [
    "scaler", 
    "scaler", 
    "scaler", 
    "scaler",
    "non-scaler", 
    "non-scaler", 
    "non-scaler",
    "non-scaler", 
    "non-scaler", 
    "non-scaler", 
    "non-scaler",
    "scaler",
    "scaler",
    "scaler",
    "scaler",
    "scaler",
    "scaler",
    "scaler",
    "scaler",
    "non-scaler",
    "non-scaler"
    # Add corresponding labels for each example
]

# Create a model pipeline
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(texts, labels)

def classify_text(text):
    processed_text = preprocess_text(text)
    return model.predict([processed_text])[0]

# New texts to classify
new_texts = [
    "I want to learn Python programming.",
    "Climate change is a major issue.",
    "I need help with my coding interview.",
    "How to start a career in data science?"
]

# Classify the new texts
classified_results = [(text, classify_text(text)) for text in new_texts]

# Create a DataFrame to display the results in a table format
df = pd.DataFrame(classified_results, columns=["Text", "Category"])

# Print the DataFrame
print(df)
