import os

DATABASE_FOLDER = os.getcwd()

class Config:

  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATABASE_FOLDER, 'sqlite.db')
  SECRET_KEY = '1b27a240570323a8abb79a569f3414cdb59a171b'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
