#### Music Organization CLI
This is a CLI tool written in Python with some simple commands which solve a few problems for myself regarding organizing my personal music library.

To-do:
To 'complete' this project, I think there needs to be a smooth flow between getting album info (musicorg \[-gi/--getInfo]), adding metadata tags with said info (musicorg \[-am/-editAlbumMetadata], musicorg \[-tm/editTrackMetadata]), and then reformatting song titles to add track indices (musicorg \[-r/--reformat]). 
The final step for this would be modifying 'reformat' to use track indices from ID3 tags if they exist, and prompting the user to input them (as usual) if they don't.