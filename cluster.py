import os
import math
import copy
import logging
    
class SongDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    
    def __repr__(self):
      return unicode("%s by %s" % (self.title, self.artist))
    
#---------------------------------------------------------------
class MusicClusterer(object):
  
  def __init__(self):
    self.logger = logging.getLogger("Clusterer")
    
  #-------------------------------------------------------------

  def cluster(self, objects):
    
    first_clusters = []
    
    for x in objects:
      first_clusters.append(Cluster([SongDict(**x)]))
      
    return self.__cluster_impl(first_clusters)
    
  #-------------------------------------------------------------
      
  def __cluster_impl(self, clusters):
    
    #make sure there is some work to do
    if(len(clusters)  < 2):
      return clusters[0]
    
    todo = copy.copy(clusters)
    new_sets = []
    
    for x in clusters:
      #skip clusters we have already seen
      if x not in todo:
        continue
      
      nearest_dist = float("inf")
      n = None
      
      for y in todo:
        
        #no self comparisons
        if(y == x): continue
        
        dist = x.distance(y)
        
        if( dist < nearest_dist ):
          n = y
          nearest_dist = dist
      
      #pop the nearest element from todo
      todo.remove(x)
      
      if n == None:
        new_sets.append( Cluster([x]) )
      else:
        todo.remove(n)
        new_sets.append( Cluster([x,n]) )
    
    #cluster new sets
    return self.__cluster_impl(new_sets)
  
  
  def display_songs(self, c):
    
    if( isinstance(c, Cluster) ):
      for d in c.data:
        self.display_songs(d)
    else:
      print "%s - %s " % (c.title, c.artist)
    
#---------------------------------------------------------------
class Cluster:
  
  tags = None
  
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
    
    if(self.tags == None):
      self.tags = []
      
      for d in self.data:
          self.tags.extend(d.tags)
  
    return self.tags
  
  
  def __repr__(self):
    return unicode(self.data)