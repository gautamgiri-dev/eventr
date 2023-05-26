from django.shortcuts import render, redirect
from datetime import datetime
import json

def index(request):

    def modify_datetime(dt):
        return datetime.fromisoformat(dt).strftime("%A %d %B, %Y %I:%M %p")

    context = json.loads(request.session.get('events_data', '{}'))

    if not context:
        return redirect('/')

    for event in context['events']:
        start = event['start']
        end = event['end']
        event['start']['dateTime'] = modify_datetime(start['dateTime']) if 'dateTime' in start else 'NA'
        event['end']['dateTime'] = modify_datetime(end['dateTime']) if 'dateTime' in end else 'NA'

    # reversing events list to get latest events on top
    context['events'] = context['events'][::-1]

    return render(request, 'events.html', context=context)
