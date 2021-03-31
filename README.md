# Youtube converter api
## Introduction
This API allows users to send an URL to YouTube media from which the audio track will be downloaded.
In return user receives token to download a requested audio file.
## Table of contents
1. [Requirements & launch](#requirements-&-launch)
2. [Endpoints](#endpoints)
3. [Access manager](#access-manager)
4. [Constants](#constants)
5. [Dependencies](#dependencies)

### Requirements & launch
Required packages are listed in `requirements.txt`. To install all of them simply type
```
pip install -r requirements.txt
```
Then the project is ready to go:
```
python3 main.py
```

### Endpoints
* GET `/`
    - Query string: `?url=<video_url>`
    - Description: Returns json with access token to downloaded audio file
    - Usage: `http://localhost:5000/?url=https://www.youtube.com/watch?v=NCFg7G63KgI`
    - Result:
```json
{
  "token": "zHTs-ellLrA8xenRHLkTE3MYxvg"
}
```

* GET `/download`
    - Query string `?token=<token>`
    - Description: Returns audio file associated with given token
    - Usage: `http://localhost:5000/download?token=zHTs-ellLrA8xenRHLkTE3MYxvg`
    - Result: start downloading a file

### Access manager
After downloading a file, generated token is put to `allowed_tokens` dictionary in `access_manager.py`.
The expiry time is set in `EXPIRY_TIME_MINUTES`, default to 5 minutes.
After starting an API, daemon thread starts in the background checking if tokens in `allowed_tokens` hasn't expired.
If so, it removes expired tokens as well as files associated with them

### Constants
All constants defined in the project are listed in `constants.py` file including downloads directory,
HTTP response codes and constants related to tokens.

### Dependencies
* [Flask](https://palletsprojects.com/p/flask/)
* [Pytube](https://python-pytube.readthedocs.io/en/latest/api.html)