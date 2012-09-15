import mutagen
import os
import mpd
import sys
import logging
import pylast

API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"

if __name__ == "__main__":
  logging.basicConfig()
  
  
  if(len(sys.argv) < 2):
    
    if(len(sys.argv) > 2):
      port = 6600
    else:
      port = sys.argv[2]
    
    client = MPDClient()
    client.connect(host=sys.argv[1], port=port)
  
  else:
    print "Usage: %s <host> [port]" % sys.argv[0]