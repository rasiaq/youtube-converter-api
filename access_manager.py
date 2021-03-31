from datetime import datetime, timedelta
import time
import os
import constants

allowed_tokens = {}
audio_files = {}


def add_token(token, file):
    """
    Adds token with expiration date to allowed_tokens and token with file name to audio_files
    :param token: generated access token
    :param file: audio file name
    :return:
    """
    expiry_date = datetime.now() + timedelta(minutes=constants.EXPIRY_TIME_MINUTES)
    allowed_tokens[token] = expiry_date
    audio_files[token] = file


def has_access(token):
    """
    Checks if token exists in allowed_tokens
    :param token: access token
    :return: True if is present in allowed_tokens, False otherwise
    """
    return token in allowed_tokens


def is_valid(token):
    """
    Checks if token has not expired
    :param token: access token
    :return: True if token expired, False otherwise
    """
    return allowed_tokens[token] >= datetime.now()


def file_assigned(token):
    """
    Checks if file is associated with a token
    :param token: access token
    :return: True if file is assigned, False otherwise
    """
    return token in audio_files


def get_audio_file(token):
    """
    Returns audio file name
    :param token: access token
    :return: audio file name
    """
    return audio_files[token]


def remove_expired_tokens():
    """
    Adds expired token to expired_tokens array, then removes them.
    Pops file names to array, which are suppose to be deleted
    :return: array of file names to be deleted
    """
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
    """
    Removes files which were previously associated with expired tokens
    :param files: file names to be deleted
    :return:
    """
    for file in files:
        os.remove(constants.DOWNLOADS_DIRECTORY + file)


def manage_tokens():
    """
    Checks if there are any expired tokens. If so, removes them and deletes a associated files
    :return:
    """
    while True:
        files = remove_expired_tokens()
        delete_expired_files(files)
        time.sleep(1)
