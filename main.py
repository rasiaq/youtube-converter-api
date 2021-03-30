import pytube
import secrets
from constants import *
import access_manager
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def download_audio():
    url = request.args.get('url')
    print(url)
    stream = pytube.YouTube(url).streams
    audio_stream = stream.get_audio_only()
    file_loc = audio_stream.download(output_path=DOWNLOADS_PATH)
    if file_loc:
        return generate_access_token(file_loc)


@app.route('/download', methods=['GET', 'POST'])
def get_audio():
    token = request.args.get('token')
    if not access_manager.has_access(token):
        return jsonify(message='Given token is invalid'), UNAUTHORIZED

    if not access_manager.is_valid(token):
        return jsonify(message='Your token has expired'), REQUEST_TIMEOUT

    if not access_manager.file_exists(token):
        return jsonify(message='Your mp3 could not be found'), NOT_FOUND

    try:
        audio_file = access_manager.get_audio_file(token)
        return send_from_directory('', filename='', as_attachment=True)
    except FileNotFoundError:
        return jsonify(message='An error has occurred'), NOT_FOUND


def generate_access_token(file):
    token = secrets.token_urlsafe(20)
    access_manager.add_token(token, file)
    return jsonify(token)


app.run()
