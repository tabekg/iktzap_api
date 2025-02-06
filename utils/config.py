from utils.parsers import Config

config = Config()

MODE = config.get('system', 'mode')
IS_DEBUG_MODE = MODE == 'dev'
DB_URL = config.get('system', 'db_url')
API_URL = config.get('system', 'api_url')
API_VERSION = config.get('system', 'api_version')
WEB_URL = config.get('system', 'web_url')
PORT = config.get('system', 'port')

SECRET_KEY = config.get('system', 'secret_key')
ACCESS_TOKEN_EXPIRE_DAYS = 90
STORAGE_PATH = config.get('system', 'storage_path')
STORAGE_DIRECTORIES = ['images']

ITEMS_ON_PER_PAGE = 30
IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif', 'pdf', 'heic'}
