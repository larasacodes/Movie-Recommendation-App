import requests
import json

def get_movie_details(movie_id):
    response = requests.get(f"https://api.watchmode.com/v1/title/{movie_id}/sources/?apiKey={YOUR API KEY HERE}")
    details_data = response.json()
    return details_data

genre_ids = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science fiction": 878,
    "tv movie": 10770,
    "thriller": 53,
    "war": 10752,
    "western": 37
}

genre_choice = input("What kind of movie would you like to watch? (comedy, thriller, horror) ")

params = {
    "api_key": "{YOUR API KEY HERE}",
    "include_adult": False,
    "include_video": False,
    "language": "en-US",
    "page": 1,
    "sort_by": "popularity.desc", # see if you can change it to sort be something else
    "with_genres": genre_ids.get(genre_choice)
    }
response = requests.get("https://api.themoviedb.org/3/discover/movie", params = params)

data = response.json()["results"]

#print(json.dumps(data, indent=4))

for index, result in enumerate(data[:10]):
    print(f"{index + 1:>2d}. {result["title"]:<25s} >>> {result["overview"]}")

user_choice = input("Enter the number of the movie you want to find out more about: ")

if user_choice in map(str, range(1, 11)):
    chosen_index = int(user_choice) - 1
    tmdb_id = data[chosen_index]["id"]
    watchmode_params = {
        "apiKey": "{YOUR API KEY HERE}",
        "search_field":"tmdb_movie_id",
        "search_value": tmdb_id
    }
    watchmode_response = requests.get("https://api.watchmode.com/v1/search/", params = watchmode_params)
    watchmode_id = watchmode_response.json()["title_results"][0]["id"]
    watchmode_details = get_movie_details(watchmode_id)
    print(watchmode_details)
else:
    print("That wasn't one of the options!")
