import argparse
import os
from organizer.organizer import Organizer

def main():
    parser = argparse.ArgumentParser(description="Music Organization Tool")
    parser.add_argument("-r", "--reformat", action="store_true", 
                        help="Add indices to music files in an album folder")
    parser.add_argument("-gi", "--getInfo", action="store_true", 
                        help="Lookup artist or album details, using the MusicBrainz API")
    parser.add_argument("-ca", "--createAlbum", action="store_true", 
                        help="Moves files ending with a given extension in a specified directory to a new album folder in the current working directory.")
    parser.add_argument("-am", "--editAlbumMetadata", action="store_true", 
                        help="Edit the MP3 metadata for songs in the current working directory. Must be called with --artist, --album, and/or --year to make changes")
    parser.add_argument("-tm", "--editTrackMetadata", action="store_true",
                        help="Edit the MP3 metadata for the tracks in the current working directory.")
    parser.add_argument("--artist", type=str, 
                        help="Set the artist name for metadata editing (album only)")
    parser.add_argument("--album", type=str, 
                        help="Set the album title for metadata editing (album only)")
    parser.add_argument("--year", type=str, 
                        help="Set the album's release year for metadata editing (album only)")
    
    args = parser.parse_args()

    org = Organizer(os.getcwd())

    if args.reformat:
        org.reformat()
    elif args.getInfo:
        org.getInfo()
    elif args.createAlbum:
        org.createAlbum()
    elif args.editAlbumMetadata:
        org.editAlbumMetadata(artist_name=args.artist, album_name=args.album, album_year=args.year)
    elif args.editTrackMetadata:
        org.editTrackMetadata()
    

if __name__ == "__main__":
    main()