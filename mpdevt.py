import mpd
import threading
import logging
import time

'''
To enable the decision system and learning system to listen for MPD events, I wrote an MPD event dispatcher.

'''

#number of seconds between server checks
POLLING_INTERVAL = 0.5

class PollingMPDClient():
  
  running = False
  
  def __init__(self):
    self.logger = logging.getLogger("MPDClient")
    self.client = mpd.MPDClient()
  
  
  def connect(self, host, port=6600, password=None):
    '''Connect to an MPD instance and poll'''
    self.logger.info("Now connecting to %s:%d...",host,port))
    self.client.connect(host=host, port=port)
    
    if(password != None):
      self.logger.info("Authenticating...")
      self.client.password(password)
    else:
      self.logger.info("No password provided, skipping authentication")
      
    #start the main loop
    
    
  def run_poller(self):
    '''This is the main poller that gets events and feeds them back
    '''
    
    while self.running:
      time.sleep(POLLING_INTERVAL)