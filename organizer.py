import os
import shutil

class Organizer():
    def __init__(self, directory):
        self._directory = directory

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
        try:
            files = os.listdir(album_folder)
            for item in files:
                if (item[-4:] != ('.mp3' or '.wav')) or (item[-5:] != '.flac'):
                    print("Error: Album folder contains extraneous folders")
            for index, file in enumerate(files, start=1):

                filename, fileExt = os.path.splitext(file)
                new_name = format.format(index = index, name = filename) + fileExt

                source_path = os.path.join(album_folder, file)
                new_path = os.path.join(album_folder, new_name)6
                shutil.move(source_path, new_path)
                print(f"Renamed {file} to {new_name}!!!")
        except FileNotFoundError:
            print("Error: The given directory does not exist.")

        
        


    def organize(self):
        files = [i for i in os.scandir(path=self._directory)]
        for item in files:
            if item.is_dir():
                files = [i for i in os.scandir(item.path)]
                print(files)

            else:
                files = item
                print(item)


if __name__ == "__main__":
    organizer = Organizer('.')
    organizer.addIndex()

