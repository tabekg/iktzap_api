import os
import random
import string
from datetime import datetime

from werkzeug.utils import secure_filename

from utils.config import STORAGE_PATH, STORAGE_DIRECTORIES


def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = {}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file(file, folder):
    ym = datetime.now().strftime("%Y/%m")
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(4))
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + '_' + rand_string + '_' + secure_filename(file.filename)
    directory = str(os.path.join(STORAGE_PATH, folder, ym))
    if not os.path.exists(directory):
        os.makedirs(directory)
    file.save(os.path.join(directory, filename))
    return ym + '/' + filename


def delete_file(file_path, folder):
    if folder not in STORAGE_DIRECTORIES:
        raise ValueError()
    path = os.path.join(STORAGE_PATH, folder, file_path)
    if os.path.exists(path):
        os.remove(path)
