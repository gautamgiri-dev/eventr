from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView
"""
    Rest App can be modularized to sub apps e.g.
        Rest
            -v1
                -calendar => logic for handling calendar endpoints
    for better maintainability and scalability
"""
urlpatterns = [
    path('v1/calendar/init/', GoogleCalendarInitView, name='google_calendar_init'),
    path('v1/calendar/redirect/', GoogleCalendarRedirectView, name='google_calendar_redirect'),
]