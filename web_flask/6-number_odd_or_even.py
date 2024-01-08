#!/usr/bin/python3
"""
launch the Flask web application
    listen on 0.0.0.0 at port 5000
    routes: /:                    shows "Hello HBNB!"
            /hbnb:                shows "HBNB"
            /c/<text>:            shows "C" + text (replace "_" with " ")
            /python/<text>:       shows "Python" + text (default="is cool")
            /number/<n>:          shows "n is a number" only if int
            /number_template/<n>: shows HTML page only if n is int
            /number_odd_or_even/<n>: show HTML page and odd or even info
"""

from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """shows text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """shows text"""
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
    """shows text if int is provided."""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def html_if_int(n):
    """html to be displayed if int supplied
       supplied integer into the HTML template
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def html_odd_or_even(n):
    """html page to display if int is provided
       the supplied integer into the HTML template
       replace text to show int is even or odd
    """
    odd_or_even = "even" if (n % 2 == 0) else "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, odd_or_even=odd_or_even)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
