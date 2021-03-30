from datetime import datetime, timedelta

allowed_tokens = {}
files_locations = {}


def add_token(token, file):
    expiry_date = datetime.now() + timedelta(minutes=5)
    allowed_tokens[token] = expiry_date
    files_locations[token] = file


def has_access(token):
    return token in allowed_tokens


def is_valid(token):
    return allowed_tokens[token] >= datetime.now()


def file_exists(token):
    return token in files_locations


def get_audio_file(token):
    return files_locations[token]