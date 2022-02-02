# NOTify script
# Jace Simons - 2/1/22
# Scrape banned FRC Competition songs from the spreadsheet and dump them into a spotify playlist using Selenium web auto
# It is assumed that a spotify search will yield the correct song and not one with the same name.

# the os allows access to env vars
import os

# requests and urllib are for interaction with spotify api
import requests

# set the api token to the env var
api_token = os.getenv('SPOTIFY_AUTH_TOKEN')

# initialize file_name to be DoNotPlayList.txt, which is assumed to be in scope of directory. This file is a stripped
# down version of the original spreadsheet, but only contains the column of song names to avoid from parsing.
file_name = "DoNotPlayList.txt"


# open_file handles opening the list of banned songs (file updated as of 2/1/22)
def open_file(file_name):
    # try ...
    try:
        # ... opening the file
        file_handler = open(file_name)
        # tell the user that the current file is (file_name)
        print("Working file: " + file_name)
        return file_handler
    # if it throws an exception
    except:
        # tell the user and exit
        print("Invalid file name; try again")
        exit()


# search_for_song takes in the line (which contains the name of the artist + the song title) and search for it on the
# Spotify web api
def search_for_song(search_string):
    # set the working url to the search api, and inject the query
    # result_type = ["track"]
    query = f"https://api.spotify.com/v1/search?query=track%3A{search_string}+artist%3A&type=track&offset=0&limit=20"
    # query = f"https://api.spotify.com/v1/search?query=track%3A{search_string}+&type={result_type}&offset=0&limit=20"
    # # response is an object to interact with the spotify web API
    response = requests.get(
        query,
        # headers are required by the spotify API and are injected as json
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(api_token)
        }
    )
    # instantiate response_json object to store the data returned from our search
    response_json = response.json()
    print(response_json)
    results = response_json["tracks"]["items"]

    uri = results[0]["uri"]
    return uri

    # # store results by calling the response json from above with the key 'tracks' and value 'items' pair
    # # results = response_json['tracks']['items']
    # # if results is not empty ...
    # if results:
    #     # ... store the first result and return it
    #     # this code assumes the first song is the correct one, given we are searching for it using the song name and the
    #     # artist's name
    #     return results[0]['id']
    # # if results is empty
    # else:
    #     # throw exception
    #     raise Exception(f"{search_string} yielded no results.")


# function to add the song to the do not playlist, taking in the raw line from the file parser
def add_song_to_playlist(raw_line):
    # the playlist url is hardcoded because we are accessing a specific playlist
    playlist_url = "https://api.spotify.com/v1/playlists/2q6kfPEBIefmk3BlhC93Ee/tracks"
    # using the response object, put the song into the playlist
    response = requests.put(
        # playlist url is the working url
        playlist_url,
        # inject json
        json={
            # the song id is returned by searching for the song with the raw search term from the text file
            "ids": [search_for_song(raw_line)]
        },
        # once again, the headers are required by the spotify api
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
    )
    # return boolean of whether the response object contains something
    return response.ok


# parse the text file to extract the artist name + song title
def parse_text_file():
    # counter to keep track of lines analyzed
    count = 0
    # go line by line through the file returned by open_file
    for line in open_file(file_name):
        print(line)
        # take the line (which consists of song title and artist name) and pass it to the add_song_to_playlist function
        add_song_to_playlist(line)
        # increment counter
        count += 1


# call the parse_text_file function to effectively start the program
parse_text_file()
