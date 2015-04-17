from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import flask

# Google Drive stuff
import httplib2
import pprint
import json
from apiclient import discovery
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client.file import Storage
from google.appengine.api import users

CLIENT_ID = '67639165534-iat1fois0eu3u0uq7cfn3fano7nemetq.apps.googleusercontent.com'
CLIENT_SECRET = 'fCI3SAnwZS8NuJA78uQWDY0k'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# configuration
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login')
def login():
    user = users.get_current_user()
    if user:
        return flask.redirect('/user/overview')
    else:
        return flask.redirect(users.create_login_url('/user/overview'))


@app.route('/user/overview')
def user():
    return render_template('overview.html', logout_url = users.create_logout_url('/'))

@app.route('/wipe')
def wipe():
    del flask.session['credentials']
    return flask.redirect(flask.url_for('user'))


@app.route('/user/goals')
def goals():
    """return render_template('goals.html')"""

    # if 'credentials' not in flask.session:
    #     return flask.redirect(flask.url_for('oauth2callback'))
    # credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    # if credentials.access_token_expired:
    #     return flask.redirect(flask.url_for('oauth2callback'))

    # else:
    #     goals_id = "0B7e5dn7QCphMU3F4RFcxMkVDSk0"
    #     http_auth = credentials.authorize(httplib2.Http())
    #     drive_service = discovery.build('drive', 'v2', http_auth)
    #     goals = drive_service.files().get_media(fileId = goals_id).execute()
    mock_goal_data = [0, 200, 400, 600, 800, 1000,
                      1200, 1400, 1600, 1800, 2000]
    mock_goals = [{"title": "hello", "due_date": "today!", "price": "2000",
                   "data": mock_goal_data}]
    return render_template('goals.html', goals=mock_goals)


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/drive',
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('goals'))


if __name__ == '__main__':
    app.run(debug=True)
