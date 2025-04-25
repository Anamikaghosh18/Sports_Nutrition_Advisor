import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-for-sports-analyzer')
 
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    

    @staticmethod
    def init_app():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)