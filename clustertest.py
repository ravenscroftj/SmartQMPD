import cluster
import pylast
import os
from mutagen.easyid3 import EasyID3

API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

def gather_data( path ):
  
  metadata = []
  
  #walk the directory looking for music
  for root, dirs, files in os.walk(path):
    for file in files:
      if(file.endswith(".mp3")):
	metadata.append(process_file(os.path.join(root,file)))

  return metadata

def process_file( file_path ):
  '''Process a file and get metadata'''
  e = EasyID3( file_path )
  return e

if __name__ == "__main__":
  files = gather_data("/home/james/tmp/")
  
  for f in files:
    print f['title'][0] + " - " + f['artist'][0]