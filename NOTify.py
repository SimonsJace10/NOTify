# NOTify script
# Jace Simons - 2/1/22
# Scrape banned FRC Competition songs from the spreadsheet and dump them into a spotify playlist using Selenium web auto
# It is assumed that a spotify search will yield the correct song and not one with the same name.

# selenium provides basic API access to do web automation tasks
# in this project, it is used to interact with the spotify web player
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# initialize file_name to be DoNotPlayList.txt, which is assumed to be in scope of directory. This file is a stripped
# down version of the original spreadsheet, but only contains the column of song names to avoid from parsing.
file_name = "DoNotPlayList.txt"

# the webdriver is a file published by selenium which allows for automation of a specific browser - in this case Chrome
driver = webdriver.Chrome(r'chromedriver.exe')


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


def add_song_to_playlist(song_name):
    # take in a song name and search for it on the Spotify web player
    # then, add it to the playlist

    driver.get('https://open.spotify.com/search')
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[3]/div/div/form/input').\
        context_click()


def fetch_and_search_song_name():
    count = 0
    # go line by line through the file from open_file
    for line in open_file(file_name):
        # take the song name and pass it to the add_song_to_playlist function
        add_song_to_playlist(line)
        count += 1


def login():
    driver.get('https://open.spotify.com/')
    driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[5]/button[2]').click()
    driver.find_element(By.CSS_SELECTOR, '#login-username').click().send_keys('stickyscissors15')
    driver.find_element(By.CSS_SELECTOR, '#login-password').click.send_keys('DummyPass1234')
    driver.find_element(By.XPATH, '//*[@id="login-button"]/div[1]').click()


login()
#fetch_and_search_song_name()
#driver.quit()
