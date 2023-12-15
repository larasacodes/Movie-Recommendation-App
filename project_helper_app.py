import requests
import json
import random
import csv
from urllib.request import urlopen
from flask import Flask, render_template, request

#use that to make a new server
app = Flask(__name__)

def get_movie_details(movie_id):
    response = requests.get(f"https://api.watchmode.com/v1/title/{movie_id}/sources/?apiKey={YOUR API KEY HERE}")
    details_data = response.json()
    return details_data

url = urlopen('https://api.watchmode.com/datasets/title_id_map.csv')
spreadsheet = list(csv.reader(url.read().decode('utf-8').splitlines()))
def get_random_wm_id():
    row_index = random.randint(0, len(spreadsheet) - 1)
    row = [spreadsheet[row_index][i] for i in range(len(spreadsheet[row_index]))]
    wm_id = row[0]
    return wm_id

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

#genre_choice = input("Do you know what kind of movie you would like to watch? (comedy, thriller, horror...) If you would like to search for a title, type 'no', or enter 'surprise me':  ")

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/selection', methods=['POST', 'GET'])
def selection():
    watchmode_details = []
    list_of_movies = []

    if request.method == 'POST':
        genre_choice = request.form['genre_choice']

        if genre_choice in genre_ids:
            params = {
                "api_key": "{YOUR API KEY HERE}",
                "include_adult": False,
                "include_video": False,
                "language": "en-US",
                "page": 1,
                "sort_by": "popularity.desc",  # see if you can change it to sort be something else
                "with_genres": genre_ids.get(genre_choice)
            }
            response = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)

            data = response.json()["results"]

            # print(json.dumps(data, indent=4))

            for index, result in enumerate(data[:10]):
                # print(f"{index + 1:>2d}. {result['title']:<25s} >>> {result['overview']}")
                movie_details = {
                    'title': result['title'],
                    'overview': result['overview']}
                # watchmode_details.append(movie_details)
                list_of_movies.append(movie_details)

            if 'user_choice' in request.form:
                user_choice = int(request.form['user_choice']) - 1

                if 0 <= user_choice < len(list_of_movies):
                    chosen_movie = list_of_movies[user_choice]

                    # Now you can use 'chosen_movie' for further processing
                    # For example, you can display more details about the chosen movie
                    watchmode_details = get_movie_details(chosen_movie['title'])
                    return render_template('selection.html', watchmode_details=watchmode_details, genre_choice=request.form['genre_choice'])

            return render_template('homepage.html', list_of_movies=list_of_movies, watchmode_details=watchmode_details)

        elif genre_choice == 'surprise me':
            while True:
                wm_id = get_random_wm_id()
                watchmode_params = {
                    "apiKey": "{YOUR API KEY HERE}",
                    "append_to_response": "sources"
                }
                url = f"https://api.watchmode.com/v1/title/{wm_id}/details/"
                random_response = requests.get(url, params=watchmode_params)
                rand_details = random_response.json()

                if random_response:
                    rand_details = random_response.json()
                    rand_pretty = json.dumps(rand_details, indent=4)
                    print(rand_pretty)
                else:
                    print("No details found for the random choice.")

                another_choice = input("Would you like another random choice? (yes/no): ").lower()
                if another_choice != 'yes':
                    break

            return render_template('selection.html', watchmode_details=rand_pretty)

        else:
            print("That's fine, you can type a partial title below")
            title_query = input("Enter the title (or partial title) of the movie: ")

            if not title_query:
                print("You need to provide a title.")
            else:
                params = {
                    "api_key": "{YOUR API KEY HERE}",
                    "include_adult": False,
                    "include_video": False,
                    "language": "en-US",
                    "page": 1,
                    "sort_by": "popularity.desc",
                    "query": title_query
                }

                response = requests.get("https://api.themoviedb.org/3/search/movie", params=params)

                data = response.json()["results"]

                if not data:
                    print("No movies found with that title. Please try again.")
                else:
                    for index, result in enumerate(data[:10]):
                        print(f"{index + 1:>2d}. {result['title']:<25s} >>> {result['overview']}")

                    user_choice = input("Enter the number of the movie you want to find out more about: ")

                    if user_choice in map(str, range(1, 11)):
                        chosen_index = int(user_choice) - 1
                        tmdb_id = data[chosen_index]["id"]
                        watchmode_params = {
                            "apiKey": "{YOUR API KEY HERE}",
                            "search_field": "tmdb_movie_id",
                            "search_value": tmdb_id
                        }
                        watchmode_response = requests.get("https://api.watchmode.com/v1/search/", params=watchmode_params)
                        watchmode_id = watchmode_response.json()["title_results"][0]["id"]
                        watchmode_details = get_movie_details(watchmode_id)
                        print(watchmode_details)
                    else:
                        print("That wasn't one of the options!")

            return render_template('selection.html', watchmode_details=watchmode_details)

    return render_template('selection.html')

app.run(debug=True)
