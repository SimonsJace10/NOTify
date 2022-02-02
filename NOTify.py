# NOTify script
# Jace Simons - 2/1/22
# Scrape banned FRC Competition songs from the spreadsheet and dump them into a spotify playlist using Selenium web auto
# It is assumed that a spotify search will yield the correct song and not one with the same name.

# initialize file_name to be DoNotPlayList.txt, which is assumed to be in scope of directory. This file is a stripped
# down version of the original spreadsheet, but only contains the column of song names to avoid from parsing.
file_name = "DoNotPlayList.txt"

# the webdriver is a file published by selenium which allows for automation of a specific browser - in this case Chrome
import requests
import urllib.parse

api_token = "BQD_TKuKFe1O8UTBGeTiutMqotHE6vAGgy-HEUoirIf8V6u4Eil_7n6Uib7PsGytVjg4tWOM-mjBxmn8taMwewIIKZzQ5SlnmFuSMWDN5zK" \
            "l6S0oeyKuOpKJMDT81j4Oy2PS8_uELGbgAnXdPWPiKXqgaWe-PtjS7pArZHE6KFX02OFN4mE"


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


def add_song_to_playlist(search_string):
    # take in a song name and search for it on the Spotify web player
    # then, add it to the playlist
    query = urllib.parse.quote(search_string)
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
    )
    response_json = response.json()

    results = response_json['tracks']['items']
    if results:
        return results[0]['id']
    else:
        raise Exception(f"{search_string} yielded no results.")




def fetch_song_name():
    count = 0
    # go line by line through the file from open_file
    for line in open_file(file_name):
        # take the song name and pass it to the add_song_to_playlist function
        add_song_to_playlist(line)
        count += 1


fetch_song_name()
