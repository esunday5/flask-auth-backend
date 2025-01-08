import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'xyz-old-norse-admin-2580$$')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql+pg8000://admin:aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib@dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com/ekondo'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
