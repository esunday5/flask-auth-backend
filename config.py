import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'xyz-old-norse-admin-2580$$')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+pg8000://admin:aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib@dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com/ekondo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expires in 24 hours
