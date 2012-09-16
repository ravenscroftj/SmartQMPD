'''
The track chooser logic for the queue manager

'''
import orm
import logging
import pylast
from mpdevt import mpd_listener
from sqlalchemy.orm import sessionmaker

API_KEY    = "21e7e21f732bac4749c6deb03b902cc5"
API_SECRET = "5d529e71dacfef10ae597a086a435afe"

Session = sessionmaker()

class DecisionEngine(object):
  '''Class that decides what to add to the play queue
  '''
  
  songs = {}
  
  def __init__(self, dbengine, mpdclient):
    '''Create a new mpd decision engine
    '''
    Session.configure(bind=dbengine)
    self.session = Session()
    self.client = mpdclient
    self.logger = logging.getLogger("DecisionEngine")
  
  def populate(self):
    '''Get MPD metadata from the server
    '''
    for song in self.client.listallinfo():
      
      if(song.has_key('title')):
        
        
        s = orm.Song(title=song['title'].decode("utf-8"))
        
        if(song.has_key('artist')):
          a = self.session.query(orm.Artist).filter_by(name=song['artist'].decode("utf-8")).first()
          
          if(a == None):
            a = orm.Artist(name=song['artist'].decode("utf-8"))
          
          s.artist = a
        
        #check that the song isn't already in the database
        squery = self.session.query(orm.Song).filter_by(title=['title'], artist_id=a.id)
        
        if(squery == None):
          #add song to db
          self.session.add(s)
      else:
        self.logger.info("Could not add song %s", song)
      
    #commit transaction
    self.session.commit()
      
  
  @mpd_listener('OnSongChange')
  def OnSongChange(event_type, evt):
    '''Called when the MPD client finds that a new song is playing
    '''
    #add a new track to the queue using the decision engine
    
  def ChooseTrack(self):
    '''Given a list of tracks, pick the most suitable one
    '''
    
#-------------------------------------------------------------------
    
class DecisionTree:
  
  rootNode = None
      
#-------------------------------------------------------------------

class DecisionNode:
  
  childNodes = []
  
  def evaluate(self, input_data):
    return None
    
  def decide(self):
    '''Recursively traverse the tree and return a decision'''
  
  def addChild(self, node, upper_bound=float("inf"), lower_bound=float("-inf")):
    ''' Add a decision node as a child to be conditionally evaluated
    
    Adds a new node to be evaluated iif:
    lower_bound <  self.evaluate(x) < higherbound
    '''
    self.childNodes.append( (node, upper_bound, lower_bound) )
  
  def removeChild(self, node):
    
    for n in self.childNodes:
      if n[0] == node:
        self.childNodes.remove(n)
      
#-------------------------------------------------------------------

class TagSimilarityNode(DecisionNode):
  '''Decision node used to determine the similarity of two songs from their last.fm tags
  '''
