'''
The track chooser logic for the queue manager

'''
import orm
import logging
import pylast
from mpdevt import mpd_listener

API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"


class DecisionEngine(object):
  '''Class that decides what to add to the play queue
  '''
  
  songs = {}
  
  def __init__(self, mpdclient):
    '''Create a new mpd decision engine
    '''
    self.client = mpdclient
    self.logger = logging.getLogger("DecisionEngine")
  
  def populate(self):
    '''Get MPD metadata from the server
    '''
    for song in self.client.listallinfo():
      
      if(song.has_key('title') & song.has_key('artist')):
        
        #add song to list
        self.songs[song['file']] = song
        
      else:
        self.logger.info("Could not add song %s", song)
      
      
  
  @mpd_listener('OnSongChange')
  def OnSongChange(event_type, evt):
    '''Called when the MPD client finds that a new song is playing
    '''
    #add a new track to the queue using the decision engine
    