import sys
import time
import random
import requests
import traceback
from lxml import html
import mysql.connector
from selenium import webdriver
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment

delays = [3, 5, 7, 11, 12]
baseUrl = "https://www.azlyrics.com"
sleep_counter = 0
artist_name = ""
sql_genre = "INSERT INTO genres (name) VALUES (%s)"
sql_artist = "INSERT INTO artists (name, genreId) VALUES (%s, %s)"
sql_song = "INSERT INTO songs (name, lyrics, artistId) VALUES (%s, %s, %s)"
create_tables = [
    """CREATE TABLE IF NOT EXISTS genres (
						id INTEGER PRIMARY KEY AUTO_INCREMENT,
						name VARCHAR(255)
);""",
    """CREATE TABLE IF NOT EXISTS artists (
						id INTEGER PRIMARY KEY AUTO_INCREMENT,
						name VARCHAR(255),
						genreId INTEGER,
						FOREIGN KEY(genreId) REFERENCES genres(id)
);""",
    """CREATE TABLE IF NOT EXISTS songs (
						name VARCHAR(255),
						lyrics TEXT,
						artistId INTEGER,
						FOREIGN KEY(artistId) REFERENCES artists(id)
); """
]


class Scrape:

    def __init__(self, path, user, passwd, database):
        try:
            self.driver = webdriver.Chrome(path)
            self.db = mysql.connector.connect(
                host="localhost",
                user=user,
                passwd=passwd,
                database=database
            )
            self.dbCursor = self.db.cursor()
            for i in create_tables:
                self.dbCursor.execute(i)
        except:
            print(traceback.format_exc())
            sys.exit()

    def withArtist(self, name, genre):
        global artist_name
        url = baseUrl + "/" + name[0] + "/" + name + ".html"
        artist_name = name
        self.__getSongs(self.__getLinks(url), genre)

    def withDictionary(self, dictionary):
        for genre in dictionary:
            for artist in dictionary[genre]:
                self.withArtist(artist, genre)

    def __getLinks(self, url):
        songs = dict()
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            data = soup.findAll('div', id="listAlbum")
            for div in data:
                a_tags = div.findAll('a')
                for a in a_tags:
                    songs[str(a.text)] = urljoin(baseUrl, a.get("href"))
        except:
            songs.clear()
            print("Could not get the links!")
        return songs

    def __getSongs(self, arr, genre):
        global sleep_counter
        song_counter = 0
        if len(arr) != 0:
            # CHECK GENRE IF ALREADY EXISTS OR NOT
            find_genre = "SELECT id FROM genres WHERE name= '" + genre + "'"
            self.dbCursor.execute(find_genre)
            genreId = self.dbCursor.fetchall()
            if len(genreId) == 0:
                val_genre = (genre,)
                self.dbCursor.execute(sql_genre, val_genre)
                self.db.commit()
                self.dbCursor.execute(find_genre)
                genreId = self.dbCursor.fetchall()
            genreId = genreId[0][0]

            # CHECK ARTIST IF ALREADY EXISTS OR NOT
            val_artist = random.choice(list(arr.values())).split("/")[4]
            find_artist = "SELECT id FROM artists WHERE name = '" + val_artist + "'"
            self.dbCursor.execute(find_artist)
            artistId = self.dbCursor.fetchall()
            if len(artistId) == 0:
                val_artist = (val_artist, genreId)
                self.dbCursor.execute(sql_artist, val_artist)
                self.db.commit()
                self.dbCursor.execute(find_artist)
                artistId = self.dbCursor.fetchall()
            artistId = artistId[0][0]

        for song in arr:
            try:
                # Every 50 pages wait for a minute
                if sleep_counter == 50:
                    time.sleep(60)
                    sleep_counter = 0

                # Get page source
                self.driver.get(arr[song])
                tree = html.fromstring(self.driver.page_source)
                lyrics = tree.xpath("/html/body/div[4]/div/div[2]/div[5]")
                page_source = html.tostring(lyrics[0])

                # Find and extract HTML tags, comments
                soup = BeautifulSoup(page_source, "html.parser")
                comments = soup.findAll(text=lambda text: isinstance(text, Comment))
                [comment.extract() for comment in comments]
                br_tags = soup.findAll('br')
                [br.extract() for br in br_tags]
                data = soup.find("div", attrs={'class': None, 'id': None})
                result = data.get_text().strip()

                # Add songs to the MySQL database
                val_song = (song, result, artistId)
                self.dbCursor.execute(sql_song, val_song)
                self.db.commit()
                print("add {song} to the database".format(song=song))
                song_counter += 1

                # Add delay to prevent IP ban
                time.sleep(random.choice(delays))
                sleep_counter += 1
            except:
                print("Connection Error while scraping")

        print("{count} song(s) by '{artist}' added to the '{db}' database".format(
            count=song_counter, artist=artist_name, db=self.db.database
        ))
