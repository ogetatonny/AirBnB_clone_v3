#!/usr/bin/python3
"""
launch the Flask web application
    listen 0.0.0.0 at port 5000
    routes: /:              shows "Hello HBNB!"
            /hbnb:          shows "HBNB"
            /c/<text>:      shows "C" + text (replace underscores with space)
            /python/<text>: shows "Python" + text (the default is "is cool")
"""

from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """shows text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """shows the text"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """shows text given"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """shows text given
       first route statement guarantees its functions for:
          curl -Ls 0.0.0.0:5000/python ; echo "" | cat -e
          curl -Ls 0.0.0.0:5000/python/ ; echo "" | cat -e
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def text_if_int(n):
    """shows text if int is given"""
    return "{:d} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
