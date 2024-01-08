#!/usr/bin/python3
"""
launch the Flask web application
    listen on port 5000 at 0.0.0.0
    routes: /: show "Hello HBNB!"
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """show text"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
