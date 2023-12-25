import argparse
import os
from organizer.organizer import Organizer

def main():
    parser = argparse.ArgumentParser(description="Music Organizer CLI")
    parser.add_argument("--addIndex", action="store_true", help="Add indices to music files in an album folder")
    parser.add_argument("--getInfo", action="store_true", help="Lookup artist or album details, using the musicbrainz API")
    parser.add_argument("--createAlbum", action="store_true", help="Moves files ending with a given extension in a specified directory to a new album folder in the current working directory.")

    args = parser.parse_args()

    org = Organizer(os.getcwd())

    if args.addIndex:
        org.addIndex()
    elif args.getInfo:
        org.getInfo()
    elif args.createAlbum:
        org.createAlbum()

if __name__ == "__main__":
    main()