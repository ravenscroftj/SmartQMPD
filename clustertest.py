import cluster
import pylast
import os
import json
import mpd
from mutagen.easyid3 import EasyID3
import cluster

API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

#----------------------------------------------------------------------------

def gather_mpd_data( ):
  
  music_files = []
  client = mpd.MPDClient()
  client.connect(host="localhost", port=6600)
  
  songs = client.playlistinfo()
  music_count = len(songs)
  print "There are %d tracks detected" % music_count
  
  i = 1
  for song in songs:
    print "[%d%%] %d / %d " % ( i*100/music_count , i, music_count )
    song['tags'] = get_tags(song['artist'], song['title'])
    i += 1
  return songs
#----------------------------------------------------------------------------

def gather_data( path ):
  
  metadata = []
  music_files = []
  
  #walk the directory looking for music
  for root, dirs, files in os.walk(path):
    for file in files:
      if(file.endswith(".mp3")):
        music_files.append(os.path.join(root,file))

  #now do the processing
  music_count = len(music_files)
  print "There are %d MP3 files detected" % music_count

  i = 1
  for f in music_files:
    print "[%d%%] %d / %d " % ( i*100/music_count , i, music_count )
    metadata.append( process_file(f) )
    i += 1
  return metadata

#----------------------------------------------------------------------------

def process_file( file_path ):
  '''Process a file and get metadata'''
  metadata = {}
  e = EasyID3( file_path )
  
  for key in 'title','artist','album':
    metadata[key] = e[key][0]
    
  #get the last fm data
  metadata['tags'] = get_tags(e['artist'][0], e['title'][0])
  
  return metadata

#----------------------------------------------------------------------------

def get_tags(artist , title):
 
  
  l_track = network.get_track(artist, title)
  
  tags = []
  for tag in l_track.get_top_tags():
    if(tag.weight > 20):
      tags.append(tag.item.name)
  
  return tags

#----------------------------------------------------------------------------

if __name__ == "__main__":
  
  
  
  if not(os.path.exists("/tmp/testdata")):
    data = gather_mpd_data()
    #data = gather_data("/home/james/tmp/")
    
    with open("/tmp/testdata",'w') as f:
      json.dump(data, f)
      
  else:
    
    with open("/tmp/testdata",'r') as f:
      data = json.load(f)
    
  c1 = cluster.Cluster([data[0]])
  c2 = cluster.Cluster([data[1]])
  
  print c2.distance(c1)