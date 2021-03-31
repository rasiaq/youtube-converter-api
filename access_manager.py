from datetime import datetime, timedelta
import time
import os
import constants

allowed_tokens = {}
audio_files = {}


def add_token(token, file):
    expiry_date = datetime.now() + timedelta(seconds=30)
    allowed_tokens[token] = expiry_date
    audio_files[token] = file


def has_access(token):
    return token in allowed_tokens


def is_valid(token):
    return allowed_tokens[token] >= datetime.now()


def file_exists(token):
    return token in audio_files


def get_audio_file(token):
    return audio_files[token]


def remove_expired_tokens():
    expired_tokens = []
    files_to_delete = []
    for token in allowed_tokens:
        if not is_valid(token):
            expired_tokens.append(token)
            files_to_delete.append(audio_files.pop(token))

    for expired in expired_tokens:
        del allowed_tokens[expired]

    return files_to_delete


def delete_expired_files(files):
    for file in files:
        os.remove(constants.DOWNLOADS_DIRECTORY + file)


def manage_tokens():
    while True:
        files = remove_expired_tokens()
        delete_expired_files(files)
        time.sleep(1)
