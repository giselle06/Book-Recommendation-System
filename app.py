from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load and clean dataset
df = pd.read_csv('goodreads_data.csv')
df['Genres'] = df['Genres'].apply(lambda x: ast.literal_eval(x))  # Convert string to list
df['Avg_Rating'] = pd.to_numeric(df['Avg_Rating'], errors='coerce')

# Get unique genre list
all_genres = sorted({genre for genres in df['Genres'] for genre in genres})

# Recommendation function
def recommend_by_genre(selected_genre):
    genre_books = df[df['Genres'].apply(lambda genres: selected_genre in genres)]
    top_books = genre_books.sort_values(by='Avg_Rating', ascending=False)[['Book', 'Author']].drop_duplicates()
    return top_books.head(5)

@app.route('/')
def index():
    return render_template('index.html', genres=all_genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_genre = request.form['genre']
    recommendations = recommend_by_genre(selected_genre)
    return render_template('recommendations.html', books=recommendations, genre=selected_genre)

if __name__ == '__main__':
    app.run(debug=True)
