import requests
from bs4 import BeautifulSoup

# Constants
URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_movie_list(url):
    """Fetch and parse the top movies list from the given URL."""
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    all_movies = soup.find_all(name="h3", class_="title")
    movie_titles = [movie.get_text() for movie in all_movies]
    return movie_titles[::-1]  # Reverse to get the correct order

def save_to_file(movie_list, filename="movies.txt"):
    """Save the list of movies to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        for movie in movie_list:
            file.write(f"{movie}\n")

if __name__ == "__main__":
    try:
        movies = fetch_movie_list(URL)
        save_to_file(movies)
        print("Movie list saved successfully!")
    except Exception as e:
        print(f"Error: {e}")
