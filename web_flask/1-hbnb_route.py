#!/usr/bin/python3
"""
launch the Flask web application
    listen on port 5000 at 0.0.0.0
    routes: /:     Show off "Hello HBNB!"
            /hbnb: show the "HBNB"
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """show text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display the text"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
