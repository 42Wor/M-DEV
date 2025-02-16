# functions/api/api.py
from flask import Flask
from werkzeug.wrappers import Response
from netlify_wsgi import wsgi_adapter

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Netlify Functions!"

# Your other Flask routes and logic here...

def handler(event, context):
    return wsgi_adapter(app, event, context)

if __name__ == "__main__":
    app.run(debug=True) # For local development