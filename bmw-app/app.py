from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello BMW from Flask on EKS! 🚀</h1><p>Development mode active.</p>"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
