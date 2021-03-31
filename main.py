import pytube
import secrets
import threading
import access_manager
from constants import *
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def download_audio():
    # TODO add format changing to .mp3
    """
    Requires 'url' param in query string.
    Downloads audio track from given url and saves it to specified directory in .mp4 format
    :return: previously generated access token
    """
    url = request.args.get('url')
    stream = pytube.YouTube(url).streams
    audio_stream = stream.get_audio_only()
    file_path = audio_stream.download(output_path=DOWNLOADS_DIRECTORY)
    file_name = extract_file_name(file_path)
    return generate_access_token(file_name)


@app.route('/download', methods=['GET', 'POST'])
def get_audio():
    """
    Requires 'token' param in query string
    After checking all conditions related to given token, returns audio file associated with it
    :return: audio file associated with specified token.
    If FileNotFoundError is caught, then json response with error message
    """
    token = request.args.get('token')
    if not access_manager.has_access(token):
        return jsonify(message='Given token is invalid'), UNAUTHORIZED

    if not access_manager.is_valid(token):
        return jsonify(message='Your token has expired'), REQUEST_TIMEOUT

    try:
        audio_file = access_manager.get_audio_file(token)
        return send_from_directory(ABS_DOWNLOADS_PATH, filename=audio_file, as_attachment=True)
    except FileNotFoundError:
        return jsonify(message='An error has occurred'), NOT_FOUND


def generate_access_token(file_name):
    """
    Generates access token of given length, then sends it to access_manager.add_token with associated file
    :param file_name: file name with which the token is to be associated
    :return: access token
    """
    token = secrets.token_urlsafe(TOKEN_LENGTH)
    access_manager.add_token(token, file_name)
    return jsonify(token=token)


def extract_file_name(file_path):
    """
    Extracts filename from given path
    :param file_path: absolute path to the file containing file name
    :return: filename extracted from file_path
    """
    return file_path[len(ABS_DOWNLOADS_PATH):]


def main():
    access_daemon = threading.Thread(target=access_manager.manage_tokens, daemon=True)
    access_daemon.start()
    app.run()


if __name__ == '__main__':
    main()
