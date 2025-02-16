from flask import Flask, render_template  # Import Flask again here if needed
from wsgi_adapter import WSGIAdapter

# Import your Flask app instance from app.py
from app import app as application  # Assuming your Flask app instance is named 'app' in app.py

def handler(event, context):
    # Use WSGIAdapter to handle the request and response
    return WSGIAdapter(application).handle(event, context)

# Optional: You can define your Flask app routes directly here if you prefer
# But importing from app.py is generally cleaner.
# @application.route("/another-route")
# def another_route():
#     return "This is another route handled by the function"