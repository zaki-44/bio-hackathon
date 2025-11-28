from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "Hello, Zaki!"

@app.route("/api/test")
def test():
    return jsonify({"message": "Backend is connected!", "status": "success"})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "bio-hackathon-backend"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
