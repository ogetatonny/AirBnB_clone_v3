#!/usr/bin/python3
"""
script starts Flask web app
    listen 0.0.0.0 at port 5000
    routes: /:         shows "Hello HBNB!"
            /hbnb:     shows the "HBNB"
            /c/<text>: display "C" + text (substitute underscores add space)
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """shows the text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """shows the text"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """shows the text given"""
    return "C {}".format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
