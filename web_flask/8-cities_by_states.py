#!/usr/bin/python3
"""
launch the Flask web application
    listen on 0.0.0.0 at port 5000
    routes: /:                    shows "Hello HBNB!"
            /hbnb:                shows "HBNB"
            /c/<text>:            shows "C" + text (replace "_" with " ")
            /python/<text>:       shows "Python" + text (default="is cool")
            /number/<n>:          shows "n is a number" only if int
            /number_template/<n>: shows HTML page if n is int
            /number_odd_or_even/<n>: shows HTML; shows odd and even info
            /states_list:         shows HTML and state info from storage
            /cities_by_states:    shows HTML and state city
"""
from models import storage
from models import *
from flask import Flask, render_template
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
    """shows text if int given"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def html_if_int(n):
    """shows html page if int given
       the int into html template
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def html_odd_or_even(n):
    """shows html page if int given
       place gives int for html template
       replace text to show int is odd or even
    """
    odd_or_even = "even" if (n % 2 == 0) else "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, odd_or_even=odd_or_even)


@app.teardown_appcontext
def tear_down(self):
    """Remove current SQLAlchemy session after request"""
    storage.close()


@app.route('/states_list')
def html_fetch_states():
    """shows html page
       fetch states to put into html of UL tag
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('7-states_list.html',
                           state_objs=state_objs)


@app.route('/cities_by_states')
def html_fetch_cities_by_states():
    """shows html page
       get sorted states to add to an HTML UL tag.
       get ordered cities for state into LI tag HTML file
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('8-cities_by_states.html',
                           state_objs=state_objs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
