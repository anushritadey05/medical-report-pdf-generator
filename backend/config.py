import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret Key
    SECRET_KEY = os. getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # OpenAI API (Optional - for AI summarization)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Upload folder
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # CORS
    CORS_HEADERS = 'Content-Type'