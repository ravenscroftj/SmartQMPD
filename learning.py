'''
Music database learning engine

by James Ravenscroft
'''
import logging

class LearningEngine(object):
  '''Class that does some clever stuff to help figure out what song to play next
  '''
  
  songs = {}
  
  def __init__(self):
    self.logger = logging.getLogger("LearningEngine")
  
  
  def add_track(self, songinfo):
    pass