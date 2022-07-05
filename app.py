import csv
import os

from dotenv import load_dotenv
from lyricsgenius import Genius

load_dotenv()
genius_api_key = os.getenv('GENIUS_API_KEY')

genius = Genius(genius_api_key, timeout=10)
# keywords = ["Ginobili", "Duncan", "Tony Parker", "Popovich", "San Antonio", "River walk" "Alamo"]
keywords = ["Houston"]

def getSongs(lyric):
    songNumber = 1
    for i in range(1, 50):
        print("Page: " + str(i))
        request = genius.search_lyrics(keyword, per_page=20, page=i)
        print(request)
        for hit in request['sections'][0]['hits']:
            songArtist = hit['result']['artist_names']
            songTitle = hit['result']['title']
            song = genius.search_song(songArtist, songTitle)
            try: 
                print("Song: " + str(songNumber) + "/1000")
                songNumber += 1
                print("Song title: " + song.title)
                print("Page views: " + str(hit['result']['stats']['pageviews']))
                print("Song artist: " + song.artist)
                print("Release date: " + str(song.year))
                print("Lyric: " + hit['highlights'][0]['value'])
                print('-------------------')
                writer.writerow([lyric, song.title, song.artist, song.year, hit['result']['stats']['pageviews'], hit['highlights'][0]['value']])
            except KeyError:
                writer.writerow([lyric, song.title, song.artist, song.year, "NA", hit['highlights'][0]['value']])
                continue
            except AttributeError:
                print('Missing title')
                pass
        print("~~~~🍕~~~~")

with open('houston.csv', mode='w') as f:
    fieldnames = ['Keyword','Song title', 'Artist', 'Release date', 'Page views', 'Lyrics']
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)
    for keyword in keywords:
        getSongs(keyword)
