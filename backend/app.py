# app.py
from flask import Flask
from routes.Extract import extract_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(extract_bp)

if __name__ == '__main__':
    app.run(debug=True)
