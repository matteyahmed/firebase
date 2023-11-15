import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")

try:
    # Attempt to get the default app
    default_app = firebase_admin.get_app()
except ValueError:
    # If the default app does not exist, initialize it
    default_app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://test-project-1-4cb48-default-rtdb.firebaseio.com/',
        'storageBucket': 'test-project-1-4cb48.appspot.com'
        
    })