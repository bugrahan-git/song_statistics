import numpy as np
import pandas as pd
from string import punctuation
import matplotlib.pyplot as plt

garbage_words = ["the", "a", "an", "for", "is", "are", "am",
                 "it", "of", "on", "in", "with", "for",
                 "that", "to", "at", "but", "and", "i", "i'm", "--", "[hook]", "[verse]", "[chorus]", "'n'",
                 "á", "[instrumental]", "you", "you're", "your", "me", "my", "mine", "it's", "it", "don't",
                 "yeah", "so", "oh", "all", "do", "no", "yes", "just", "be", "we", "can", "they", "he", "she", "us",
                 "this", "if", "got", "get", "what", "when", "why", "can't", "was", "were", "from", "them", "her",
                 "i'll", "uh", "not"]

sql_join_artist = """
    SELECT artists.id, artists.name, songs.name, songs.lyrics, genres.id, genres.name 
    FROM artists 
    JOIN songs ON artists.id = songs.artistId 
    JOIN genres ON artists.genreId = genres.id 
    WHERE artists.name=(%s);
"""
sql_join_genre = """
    SELECT artists.id, artists.name, songs.name, songs.lyrics, genres.id, genres.name
    FROM artists
    JOIN songs ON artists.id = songs.artistId
    JOIN genres on artists.genreId = genres.id
    WHERE genres.name=(%s);
"""


class Analysis:

    def __init__(self, db):
        self.__db = db
        self.__dbCursor = self.__db.cursor()

    def __cleanse_data(self, arr):
        result = [[song[0], song[1], song[2],
                   song[4], song[5],
                   [lyrics.lower().rstrip(punctuation) for lyrics in song[3].strip().split() if
                    lyrics.lower() not in garbage_words]] for
                  song in arr]
        return result

    def __analyze(self, arr, title):
        df = pd.DataFrame(np.array(arr), columns=["artist_id", "artist", "song",
                                                  "genre_id", "genre", "lyrics"])
        count_data_dict = self.__count_words([item for sublist in [song for song in df["lyrics"]] for item in sublist])

        count_data = pd.DataFrame.from_dict(count_data_dict, orient='index')
        count_data.columns = ["count"]
        count_data["word"] = count_data.index
        count_data = count_data.sort_values("count", ascending=False)
        self.__plot_bar(count_data, title)
        self.__plot_pie(count_data, title)

    def analyze_genre(self, genre):
        try:
            val_genre = (genre,)
            self.__dbCursor.execute(sql_join_genre, val_genre)
            result_arr = self.__dbCursor.fetchall()
            result_arr = self.__cleanse_data(result_arr)
            self.__analyze(result_arr, genre)
        except:
            print("No data found!")

    def analyze_artist(self, artist):
        try:
            val_artist = (artist,)
            self.__dbCursor.execute(sql_join_artist, val_artist)
            result_arr = self.__dbCursor.fetchall()
            result_arr = self.__cleanse_data(result_arr)
            self.__analyze(result_arr, artist)
        except:
            print("No data found!")

    # Pie chart
    def __plot_pie(self, df, title):
        explode = (0.15, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        fig1, gr = plt.subplots()
        gr.pie(df["count"].head(10), explode=explode, shadow=True, labels=df["word"].head(10), autopct='%1.1f%%', startangle=90)
        gr.axis('equal')
        title = plt.title(title)
        plt.setp(title, color="r")
        plt.show()

    # Bar chart
    def __plot_bar(self, df, title):
        df.head(20).plot(kind='bar', x='word', y='count')
        title = plt.title(title)
        plt.setp(title, color="r")
        plt.xlabel("words")
        plt.ylabel("count")
        plt.show()

    def __count_words(self, arr):
        words = dict()
        for word in arr:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
        return words
