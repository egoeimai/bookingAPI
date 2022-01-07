
from flask import Flask, request, render_template

from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
app.config["BUNDLE_ERRORS"] = True




@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
