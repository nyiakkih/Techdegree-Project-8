import requests
import csv
import re
from keys import api_key

def fetch_movie_data(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movie_data = response.json()
        return movie_data
    else:
        print(f"Failed to fetch data for IMDb ID '{imdb_id}'. Status code: {response.status_code}")
        return None

def save_movie_data(movie_data):
    try:
        title = movie_data.get('Title', 'N/A')
        runtime = int(movie_data.get('Runtime', '0').split(' ')[0])
        genre = movie_data.get('Genre', 'N/A')
        awards = movie_data.get('Awards', 'N/A')
        rated = movie_data.get('Rated', 'N/A')
        director = movie_data.get('Director', 'N/A')
        released = movie_data.get('Released', 'N/A')
        
        wins = sum(map(int, re.findall(r'(\d+) win', awards)))
        nominations = sum(map(int, re.findall(r'(\d+) nomination', awards)))

        box_office = int(movie_data.get('BoxOffice', '$0').replace('$', '').replace(',', ''))
        
        with open('movies.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title, runtime, genre, wins, nominations, box_office, rated, director, released])
        
    except ValueError:
        print(f"Error processing movie: {movie_data.get('Title', 'Unknown')}")

def main():
    with open('movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office', 'Rated', 'Director', 'Released'])
    
    with open('oscar_winners.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            imdb_id = row[1]
            movie_data = fetch_movie_data(imdb_id)
            if movie_data:
                save_movie_data(movie_data)

    print("Data saved to movies.csv")

if __name__ == "__main__":
    main()