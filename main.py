import pytube
import secrets
import threading
from constants import *
import access_manager
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def download_audio():
    url = request.args.get('url')
    stream = pytube.YouTube(url).streams
    audio_stream = stream.get_audio_only()
    file = audio_stream.download(output_path=DOWNLOADS_DIRECTORY)
    file_name = strip_file_name(file)
    return generate_access_token(file_name)


@app.route('/download', methods=['GET', 'POST'])
def get_audio():
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
    token = secrets.token_urlsafe(20)
    access_manager.add_token(token, file_name)
    return jsonify(token=token)


def strip_file_name(file):
    return file[len(ABS_DOWNLOADS_PATH):]


def main():
    access_daemon = threading.Thread(target=access_manager.manage_tokens, daemon=True)
    access_daemon.start()
    app.run()


if __name__ == '__main__':
    main()
