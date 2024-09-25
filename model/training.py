import joblib
import nltk
from nltk.corpus import movie_reviews
import os
import pandas as pd
from pathlib import Path
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Download if it's the first time using it
nltk.download('movie_reviews')

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

# Separate into two groups to build the dataframe
reviews = [" ".join(words) for words, category in documents]
sentiments = [category for words, category in documents]

df = pd.DataFrame({'review': reviews, 'sentiment': sentiments})

# lets vectorize the reviews
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
data = vectorizer.fit_transform(df['review']) 
labels = df['sentiment']

# Split for training and test
data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.2, random_state=0)

# Train the model
model = LogisticRegression()
model.fit(data_train, labels_train)

# Evaluate the model
labels_pred = model.predict(data_test)
acc = accuracy_score(labels_test, labels_pred)
report = classification_report(labels_test, labels_pred)

print(f"Accuracy: {acc}")
print(f"Classification Report:\n {report}")

# Save the model
folder_path = project_path = Path(__file__).resolve().parent
joblib.dump(model, os.path.join(folder_path, "model.pkl"))
joblib.dump(vectorizer, os.path.join(folder_path, "vectorizer.pkl")) 