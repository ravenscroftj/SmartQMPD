import mutagen
import os
import sys
import logging
import pylast
import threading

from mpdevt import PollingMPDClient, mpd_listener


API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"

@mpd_listener('OnSongChange')
def test_listener(type, evt):
  logging.info("Now playing: %s - %s", evt['title'], evt['artist'])

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  logging.info("Starting QMPD...")
  
  if(len(sys.argv) > 1):
    
    if(len(sys.argv) > 2):
      port = 6600
    else:
      port = sys.argv[2]
    
    try:
      client = PollingMPDClient()
      client.connect(host=sys.argv[1], port=port)
      l = raw_input()
    except KeyboardInterrupt:
      print "exiting..."
    
    client.running = False
  
  else:
    print "Usage: %s <host> [port]" % sys.argv[0]
    