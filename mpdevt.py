import mpd
import threading
import logging
import time

'''
To enable the decision system and learning system to listen for MPD events, I wrote an MPD event dispatcher.

'''

#number of seconds between server checks
POLLING_INTERVAL = 0.5

_event_listeners = {}

def mpd_listener( evttype ):
  ''' This is a decorator function that turns objects into MPD event listeners
  
  This decorator is used to add the given callable object to the MPD event listeners
  under a given condition
  '''
  if not(_event_listeners.has_key(evttype)):
    _event_listeners[evttype] = []
  
  return lambda x: _event_listeners[evttype].append(x)

#------------------------------------------- PollingMPDClient -------------------------------------------

class PollingMPDClient(object):
  
  currentSongID = 0
  running = False
  
  def __init__(self):
    self.logger = logging.getLogger("MPDClient")
    self.client = mpd.MPDClient()
  
  
  def connect(self, host, port=6600, password=None):
    '''Connect to an MPD instance and poll'''
    self.logger.info("Now connecting to %s:%d...", host,port)
    self.client.connect(host=host, port=port)
    
    if(password != None):
      self.logger.info("Authenticating...")
      self.client.password(password)
    else:
      self.logger.info("No password provided, skipping authentication")
      
    #start the main loop
    self.thread = threading.Thread(target=self.run_poller)
    self.thread.start()
    
    
  def run_poller(self):
    '''This is the main poller that gets events and feeds them back
    '''
    
    self.running = True
    
    while self.running:
      status = self.client.status()
      
      if(status.has_key("songid")):
        if(self.currentSongID != status['songid']):
          self.emit("OnSongChange", evt=self.client.currentsong())
          self.currentSongID = status['songid']

      time.sleep(POLLING_INTERVAL)
      
      
  def emit(self, type, *args, **kwargs):
     '''Emits event of the given type to all registered listeners'''
     
     self.logger.debug("MPDEvent: %s - %s - %s", type, args, kwargs)
     
     if(_event_listeners.has_key(type)):
       for listener in _event_listeners[type]:
         listener(type, *args, **kwargs)
       