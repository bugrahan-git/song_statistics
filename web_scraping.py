import sys
import traceback
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
import requests
import random
from selenium import webdriver
from lxml import html
import time

import mysql.connector

delays = [3, 5, 7, 11, 12]
baseUrl = "https://www.azlyrics.com"
songCounter = 0
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
        url = baseUrl + "/" + name[0] + "/" + name + ".html"
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
            print("Couldn't get the links")
        return songs

    def __getSongs(self, arr, genre):
        global songCounter
        if len(arr) != 0:
            # CHECK GENRE
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

            # CHECK ARTIST
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
        for i in arr:
            try:
                if songCounter == 50:
                    time.sleep(60)
                    songCounter = 0
                else:
                    countSongs = ("SELECT COUNT(*) FROM songs WHERE artistId = '" + str(artistId) + "'")
                    self.dbCursor.execute(countSongs)
                    count = self.dbCursor.fetchall()
                    count = count[0][0]
                    if len(arr) > count:
                        self.driver.get(arr[i])
                        tree = html.fromstring(self.driver.page_source)
                        lyrics = tree.xpath("/html/body/div[4]/div/div[2]/div[5]")
                        page_source = html.tostring(lyrics[0])
                        soup = BeautifulSoup(page_source, "html.parser")
                        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
                        [comment.extract() for comment in comments]
                        br_tags = soup.findAll('br')
                        [br.extract() for br in br_tags]
                        data = soup.find("div", attrs={'class': None, 'id': None})
                        result = data.get_text().strip()
                        val_song = (i, result, artistId)
                        self.dbCursor.execute(sql_song, val_song)
                        self.db.commit()
                        print("add {song} to the database".format(song=i))
                        time.sleep(random.choice(delays))
                        songCounter += 1
            except:
                print("Connection Error")
