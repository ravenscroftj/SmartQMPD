'''
Music database learning engine

by James Ravenscroft
'''
import logging

from sqlalchemy.orm import sessionmaker
from mpdevt import mpd_listener

#database setup stuff
_Session = sessionmaker()

class LearningEngine(object):
  '''Class that does some clever stuff to help figure out what song to play next
  '''
  songs = {}
  
  def __init__(self, dbengine):
    self.logger = logging.getLogger("LearningEngine")
    _Session.configure(bind=dbengine)
    self.session = _Session()
  
  @mpd_listener('OnSongChange')
  def OnSongChange(event_type, evt):
    '''Called when the MPD client finds that a new song is playing
    '''
    