import os
import math

class MusicClusterer(object):
  
  def __init__(self):
    pass
  
  def cluster(self, objects):
    
    pass
  
  
class Cluster:
  
  def __init__(self, data):
    self.data = data
  
  def distance(self, cluster):
    tags_1 = self.get_tags()
    tags_2 = cluster.get_tags()
    i_1 = float(len(tags_1))
    i_2 = float(len(tags_2))
    
    x = 0.0
    
    for t in tags_1:
      if t in tags_2: x += 1
    
    return x / max( i_1, i_2 )
    
  def get_tags(self):
    tags = []
    
    for d in self.data:
      tags.extend(d['tags'])
  
    return tags
  
  