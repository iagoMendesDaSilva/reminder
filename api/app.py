import os
from routes import *
from models import *
from app.applications import app, database

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)