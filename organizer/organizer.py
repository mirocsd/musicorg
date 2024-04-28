import os
import shutil
import requests
import urllib.parse
import mutagen.id3
import mutagen.mp3
from api_key import API_KEY

class Organizer():
    def __init__(self, directory="."):
        self.directory = directory

    def createAlbum(self):
        extensions = input("Please enter the file extension(s) you would like to move into the new folder (e.g. mp3, wav): ").split()
        album_directory = input("Please enter the directory containing the files to be moved (blank if current working directory): ")
        if album_directory in [None, "", " "]:
            album_directory = os.getcwd()
        for i in range(len(extensions)):
            extensions[i] = extensions[i].strip()
        new_album = input("Enter the name of the new album folder: ")
        new_album_folder = os.path.join(os.getcwd(), f'./{new_album}')
        os.makedirs(new_album_folder, exist_ok=True)

        files = os.listdir(album_directory)

        for file in files:
            if file.lower().split('.')[1] in extensions:
                source_path = os.path.join(album_directory, file)
                destination_path = os.path.join(new_album_folder, file)
                shutil.move(source_path, destination_path)
                print(f"--- Moved {file} to {new_album_folder}. ---")
        
        print("*** Album folder created. ***")


    def rename_file(self, file, album_folder, new_name):
        source_path = os.path.join(album_folder, file)
        new_path = os.path.join(album_folder, new_name)
        shutil.move(source_path, new_path)
        print(f"Renamed {file} to {new_name}!")


    def reformat(self):
        album_folder = input("Enter the relative or absolute directory of your album folder, containing only .wav or .mp3 files (. if current directory):\n")
        format = input("Enter the desired song format (e.g. {index} - {name}, {name} {index}, {name} etc.):\n")
        Invalid = True
        while Invalid:
            try:
                num_removed = int(input("Remove X characters from the start of each track name (0 if none): "))
                Invalid = False
            except ValueError:
                print("Error: Please enter an integer value.")

        try:
            files = os.listdir(album_folder)
                
        
            for index, file in enumerate(files, start=1):
                filename, fileExt = os.path.splitext(file)
                if fileExt == ".mp3" or ".wav":
                    if num_removed is None:
                        new_name = format.format(index = index, name = filename) + fileExt
                    else:
                        new_name = format.format(index=index, name=filename[num_removed:].strip()) + fileExt

                self.rename_file(file, album_folder, new_name)

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


    def editAlbumMetadata(self, artist_name=None, album_name=None, album_year=None):
        directory = os.getcwd()
        mp3_files = [i for i in os.listdir(directory) if i.endswith('.mp3')]
        for file in mp3_files:

            f_path = os.path.join(directory, file)
            audio = mutagen.mp3.MP3(f_path)
            
            if audio.tags is None:
                audio.tags = mutagen.id3.ID3()


            if artist_name:
                audio.tags['TPE1'] = mutagen.id3.TPE1(encoding=3, text=artist_name)
            if album_name:
                audio.tags['TALB'] = mutagen.id3.TALB(encoding=3, text=album_name)
            if album_year:
                audio.tags['TYER'] = mutagen.id3.TYER(encoding=3, text=album_year)

            audio.save(f_path, v2_version=3, v1=0)

        print("***Album/artist metadata editing complete***")

        if input("Edit metadata for each track (song title, track number)? (y/n): ").strip() == "y":
            print("Assuming all mp3 files in the current directory are part of the same album.")
            
            print("--------------")
            tr_is_fn = True if input("Take track names as filenames (excluding .mp3)? ").strip() == "y" else False
            print("--------------")
            print("Beginning track metadata editing.")
            print("--------------")
            for file in mp3_files:
                num = input(f"Enter the track number for {file[:-4]}")
                if tr_is_fn:
                    self.editTrackMetadata(track=file, track_title=file[:-4], track_num=num)
                    
                else:
                    self.editTrackMetadata(track=file)


    def editTrackMetadata(self, track=None, track_title=None, track_num=None):
        if not track:
            track = input("Enter the track's full filename in the current working directory")
        if not track_title:
            track_title = input("Enter the track title: ").strip()

        while True:
            if not track_num:
                track_num = input("Enter the track number: ").strip()
            if track_num.isdigit():
                break
            else:
                print("Error: Input should be integers only.")
                track_num = input("Enter the track number: ").strip()

        f_path = os.path.join(os.getcwd(), track)
        audio = mutagen.mp3.MP3(f_path, v2_version=3)

        if audio.tags is None:
            audio.tags = mutagen.id3.ID3()

        audio['TIT2'] = mutagen.id3.TIT2(encoding=3, text=track_title)
        audio['TRCK'] = mutagen.id3.TRCK(encoding=3, text=str(track_num))
        audio.pprint()
        audio.save(f_path, v2_version=3)
