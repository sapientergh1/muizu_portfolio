import os
import sys
import django
from flask import Flask, request, Response
from flask_cors import CORS
from django.core.wsgi import get_wsgi_application
from django.conf import settings
import threading
from werkzeug.serving import make_server

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muizu_portfolio.settings')

# Setup Django
django.setup()

# Get the Django WSGI application
django_app = get_wsgi_application()

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_to_django(path):
    """Proxy all requests to Django application"""
    from werkzeug.test import Client
    from werkzeug.wrappers import BaseResponse
    
    # Create a test client for Django app
    client = Client(django_app, BaseResponse)
    
    # Forward the request to Django
    response = client.open(
        path='/' + path,
        method=request.method,
        headers=list(request.headers),
        data=request.get_data(),
        query_string=request.query_string
    )
    
    # Return the Django response through Flask
    return Response(
        response.get_data(),
        status=response.status_code,
        headers=dict(response.headers)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

