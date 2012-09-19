'''

Database stuff for the clustering application

'''
import logging

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def init(engine):
  ''' Given a db engine, create the relevent tables
  '''
  Base.metadata.create_all(engine)

#---------------------------------------------------------------

artist_tags = Table('artist_tags', Base.metadata,
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

#---------------------------------------------------------------

album_tags = Table('album_tags', Base.metadata,
    Column('album_id', Integer, ForeignKey('albums.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

#---------------------------------------------------------------

song_tags = Table('song_tags', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)
  
#---------------------------------------------------------------

class Tag(Base):
  
  __tablename__ = 'tags'
  
  id  = Column(Integer, primary_key=True)
  tag = Column(String)

#---------------------------------------------------------------

class Artist(Base):
  
  __tablename__ = 'artists'
  
  id = Column(Integer, primary_key=True)
  name = Column(String)
  songs = relationship("Song", backref="artist")
  albums = relationship("Album", backref="artist")
  tags = relationship("Tag", secondary=artist_tags, backref="artists")
  
#---------------------------------------------------------------

class Album(Base):
  __tablename__ = 'albums'
  
  id = Column(Integer, primary_key=True)
  title = Column(String)
  artist_id = Column(Integer, ForeignKey('artists.id'))
  tags = relationship("Tag", secondary=album_tags, backref="albums")
  
#---------------------------------------------------------------

class Song(Base):
  
  __tablename__ = 'songs'
  
  id = Column(Integer, primary_key=True)
  title  = Column(String)
  artist_id = Column(Integer, ForeignKey('artists.id'))
  album_id  = Column(Integer, ForeignKey('albums.id'))
  tags = relationship("Tag", secondary=song_tags, backref="songs")

#---------------------------------------------------------------