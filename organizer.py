import os
import shutil
import requests
import urllib.parse

API_KEY = '0d1d6652505b51dc51b0079c72c5d94c'

class Organizer():
    def __init__(self, directory):
        self.__directory = directory

    def createAlbum(self, album_directory, extension):
        album = input("Enter the name of the new album folder: ")
        album_folder = os.path.join(os.getcwd(), f'./{album}')
        os.makedirs(album_folder, exist_ok=True)

        files = os.listdir(album_directory)

        for file in files:
            if file.lower().endswith(extension):
                source_path = os.path.join(album_directory, file)
                destination_path = os.path.join(album_folder, file)
                shutil.move(source_path, destination_path)
                print(f"--- Moved {file} to {album_folder}. ---")
        
        print("*** Album folder created. ***")

    def addIndex(self):
        album_folder = input("Enter the relative or absolute directory of your album folder, containing only .wav or .mp3 files:\n")
        format = input("Enter the desired song format (e.g. {index} - {name}, {name} {index}, etc.):\n")
        strip_spec = input("Strip existing special characters or numbers? (Y/N)\nUse if song names are in a different format AND proper song names do not contain special chars or numbers (these will be removed) : ")
        Invalid = False
        try:
            files = os.listdir(album_folder)
            while not Invalid:
                for item in files:
                    if (item[-4:] != ('.mp3' or '.wav')) or (item[-5:] != '.flac'):
                        print("Error: Album folder contains extraneous folders")
                        Invalid = True
                        break
                if Invalid:
                    break
                if strip_spec.lower().strip() == 'y':
                    for index, file in enumerate(files, start=1):
                        filename_strip = ''
                        filename, fileExt = os.path.splitext(file)
                        plaus_chars = "abcdefghijklmnopqrstuvwxyz"
                        for char in filename:
                            if char in plaus_chars or plaus_chars.upper():
                                filename_strip.join(char)
                        
                        new_name = format.format(index = index, name = filename_strip) + fileExt

                        source_path = os.path.join(album_folder, file)
                        new_path = os.path.join(album_folder, new_name)
                        shutil.move(source_path, new_path)
                        print(f"Renamed {file} to {new_name}!")
                
                else:
                    for index, file in enumerate(files, start=1):

                        filename, fileExt = os.path.splitext(file)
                        new_name = format.format(index = index, name = filename) + fileExt

                        source_path = os.path.join(album_folder, file)
                        new_path = os.path.join(album_folder, new_name)
                        shutil.move(source_path, new_path)
                        print(f"Renamed {file} to {new_name}!")
        except FileNotFoundError:
            print("Error: The given directory does not exist.")

        
    def getInfo(self):
        type = input("Please enter the info you would like (artist or release): ").lower().strip()
        name = input(f"Please enter the name of the {type}: ").strip()
        if type == "artist" and name:
            name = urllib.parse.quote_plus(name)
            search_results = requests.get(f'https://musicbrainz.org/ws/2/{type}?query={name}&limit=3&fmt=json').json()
            try:
                artist = search_results["artists"][0]
                print(f"Name: {artist['name']}")
                try:
                    print(f"Area: {artist['begin-area']['name']}, {artist['area']['name']}")

                except KeyError:
                    print("Area Unavailable.")

                try:
                    print(f"Years Active: {artist['life-span']['begin']}-{artist['life-span']['end']}")

                except KeyError:
                    print("Years Active Unavailable.")

                try:
                    genres = [i for i in artist['tags']]
                    genre_str = ''
                    for i in range(len(genres)):
                        genre_str += str(genres[i]['name'])
                        genre_str += ', '  

                    print(f"Genre Tags: {genre_str}")

                except KeyError:
                    print("No Genre Tags Available.")

            except IndexError:
                print("No Artist Found.")

        
        elif type == "release" and name:
            name = urllib.parse.quote_plus(name)
            search_results = requests.get(f'https://musicbrainz.org/ws/2/{type}?query={name}&limit=3&fmt=json').json()
            
            release = search_results["releases"][0]
            print(f"Artist Name: {release['artist-credit'][0]['name']}")
            try:
                print(f"Release Date: {release['release-events'][0]['date']}")
            except KeyError:
                print("No Release Date Found.")
            try:
                print(f"Record Label: {release['label-info'][0]['label']['name']}")
            except KeyError:
                print("No Label Name Found.")
            try:    
                print(f"No. of Tracks: {release['track-count']}")
            except KeyError:
                print("Number of Tracks Not Found.")

        else:
            if name:
                print("Error: Please enter a non-empty and valid type")
            elif type:
                print("Error: Please enter a non-empty album/artist name")


    def organize(self):
        files = [i for i in os.scandir(path=self.__directory)]
        for item in files:
            if item.is_dir():
                files = [i for i in os.scandir(item.path)]
                print(files)

            else:
                files = item
                print(item)

if __name__ == "__main__":
    organizer = Organizer('.')
    organizer.getInfo()

