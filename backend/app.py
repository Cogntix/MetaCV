# from flask import Flask, jsonify, request

# from routes.Extract import extract_blueprint

# app = Flask(__name__)
# @app.route('/hello', methods=['GET'])
# def hello():
#     return jsonify({"message": "Hello from Python!"})

# @app.route('/greet', methods=['POST'])
# def greet():
#     data = request.get_json()
#     name = data.get('name', 'Guest')
#     return jsonify({"message": f"Hello, {name}!"})
# # Register Blueprints
# app.register_blueprint(extract_blueprint)

# if __name__ == '__main__':
#     app.run(debug=True)

# app.py
from flask import Flask
from routes.Extract import extract_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(extract_bp)

if __name__ == '__main__':
    app.run(debug=True)
