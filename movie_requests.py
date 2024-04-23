import requests
import csv
from keys import api_key

def fetch_movie_data(imdb_id):
    url = f"http://www.omdbapi.com/?apikey={api_key}&i={imdb_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movie_data = response.json()
        return movie_data
    else:
        print(f"Failed to fetch data for IMDb ID '{imdb_id}'. Status code: {response.status_code}")
        return

def save_movie_data(movie_data_list):
    with open('movies.csv', 'w', newline='') as csvfile:
        fieldnames = ['Movie Title', 'Runtime', 'Genre', 'Award Wins', 'Award Nominations', 'Box Office']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for movie_data in movie_data_list:
            award_wins = 0
            award_nominations = 0
            
            if 'Awards' in movie_data and movie_data['Awards'] != 'N/A':
                awards = movie_data['Awards'].split(' ')
                award_wins = int(awards[0]) if awards[0].isdigit() else 0
                award_nominations = int(awards[2]) if len(awards) > 2 and awards[2].isdigit() else 0

            writer.writerow({
                'Movie Title': movie_data.get('Title', ''),
                'Runtime': movie_data.get('Runtime', '').split(' ')[0],
                'Genre': movie_data.get('Genre', ''),
                'Award Wins': award_wins,
                'Award Nominations': award_nominations,
                'Box Office': movie_data.get('BoxOffice', '').replace('$', '').replace(',', '') if movie_data.get('BoxOffice') != 'N/A' else ''
            })

def main():
    movie_data_list = []
    with open('oscar_winners.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            imdb_id = row[1]
            movie_data = fetch_movie_data(imdb_id)
            if movie_data:
                movie_data_list.append(movie_data)

    save_movie_data(movie_data_list)
    print("Data saved to movies.csv")

if __name__ == "__main__":
    main()