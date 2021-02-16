from sqlalchemy import (
    create_engine, Column, Integer, String, Date, MetaData, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# ansluta till databasen
engine = create_engine(
    'mysql+pymysql://guest:abc123@localhost/spotify',
    echo=True
)

# skapa en session for att prata med databasen
Session = sessionmaker(bind=engine)
session = Session()


# Skapa en klass som sqlalchemy senare behover for att
# skapa tabeller osv.
Base = declarative_base()


# en modell som beskriver hur varan data ska se ut
class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    release_date = Column(Date)


# en funktion som skapar "albums" tabellen om den inte redan finns
def create_tables():
    if not engine.dialect.has_table(engine, 'albums'):
        metadata = MetaData(engine)

        Table('albums', metadata,
              Column('id', Integer, primary_key=True, nullable=False),
              Column('name', String(300)),
              Column('release_date', Date))

        metadata.create_all()


# en funktion som sparar ett album i databasen
def insert_album(name, release_date):
    album = Album(name=name, release_date=release_date)
    session.add(album)
    session.commit()
    return album
