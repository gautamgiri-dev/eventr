from django.shortcuts import render, redirect
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import credentials
from googleapiclient.discovery import build
import json

def GoogleCalendarInitView(request):
    # GOOGLE_CLIENT_CONFIG should be moved to another file e.g. dotenv file or to client_secret.json file
    GOOGLE_CLIENT_CONFIG = {"web":{"client_id":"220442900074-e9i85umuaj83t33hirhopimvk8smj3il.apps.googleusercontent.com","project_id":"eventr-387909","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost:8000/rest/v1/calendar/redirect/"]}}
    flow = Flow.from_client_config(
        GOOGLE_CLIENT_CONFIG, scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/calendar.events.readonly'],
        redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
    )
    auth_url, state = flow.authorization_url(access_type='offline')
    return redirect(auth_url)

def GoogleCalendarRedirectView(request):
    code = request.GET.get('code')
    if not code:
        return redirect('/')
    
    # GOOGLE_CLIENT_CONFIG should be moved to another file e.g. dotenv file or to client_secret.json file
    GOOGLE_CLIENT_CONFIG = {"web":{"client_id":"220442900074-e9i85umuaj83t33hirhopimvk8smj3il.apps.googleusercontent.com","project_id":"eventr-387909","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost:8000/rest/v1/calendar/redirect/"]}}
    flow = Flow.from_client_config(
        GOOGLE_CLIENT_CONFIG, scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/calendar.events.readonly'],
        redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
    )

    flow.fetch_token(code=code)

    access_token = flow.credentials.token

    creds = credentials.Credentials(access_token)

    # Build the service object for the Google Calendar API
    calendar_service = build('calendar', 'v3', credentials=creds)

    # Retrieve the list of events from the primary calendar
    events_result = calendar_service.events().list(calendarId='primary').execute()
    events = events_result.get('items', [])

    # user info can be collected from any userinfo discovery endpoint
    session = flow.authorized_session()
    profile_info = session.get(
    'https://www.googleapis.com/userinfo/v2/me').json()

    SESSION_DATA = {
        'name': profile_info['name'],
        'email': profile_info['email'],
        'events': events
    }

    request.session['events_data'] = json.dumps(SESSION_DATA)

    return redirect('/events')
