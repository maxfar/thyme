from flask import Blueprint, render_template, session, redirect, url_for

import httplib2
import json
from apiclient import discovery
from apiclient.discovery import build
from oauth2client import client

goals = Blueprint('goals', __name__, template_folder='templates')

@goals.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))

    else:
        goals_id = "0B7e5dn7QCphMU3F4RFcxMkVDSk0"
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v2', http_auth)
        goals = drive_service.files().get_media(fileId=goals_id).execute()

    return render_template('goals.html', goals=json.loads(goals)['goals'])

