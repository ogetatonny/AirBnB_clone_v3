#!/usr/bin/python3
"""
launch the Flask web application
    listen on port 5000 at 0.0.0.0
    routes: /:                    show "Hello HBNB!"
            /hbnb:                show "HBNB"
            /c/<text>:            show "C" + text (replace "_" with " ")
            /python/<text>:       show "Python" + text (default="is cool")
            /number/<n>:          show "n is a number" solely if int
            /number_template/<n>: show HTML page only if n is int
            /number_odd_or_even/<n>: show HTML page; show odd/even info
            /states_list & /states:  show HTML and state info frm storage
            /cities_by_states:    show HTML and state city relations
            /states/<id>:         show HTML and state city given state id
            /hbnb_filters:        show an HTML page such as 6-index.html
"""
from models import storage
from flask import Flask, render_template
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
    """show the provided custom text"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """display the provided custom text
       initial route statement guarantees functions for:
          curl -Ls 0.0.0.0:5000/python ; echo "" | cat -e
          curl -Ls 0.0.0.0:5000/python ; echo "" | cat -e
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def text_if_int(n):
    """only show text if int is provided"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def html_if_int(n):
    """display HTML page only if the specified
       location is entered into HTML template
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def html_odd_or_even(n):
    """display the HTML page only if the given
       integer is odd or even. If integer is given
       insert the substitute text into HTML template
    """
    odd_or_even = "even" if (n % 2 == 0) else "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, odd_or_even=odd_or_even)


@app.teardown_appcontext
def tear_down(self):
    """Remove the current SQLAlchemy session request."""
    storage.close()


@app.route('/states')
@app.route('/states_list')
def html_fetch_states():
    """show HTML page, retrieve ordered
       states, and paste into UL tag
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('7-states_list.html',
                           state_objs=state_objs)


@app.route('/cities_by_states')
def html_fetch_cities_by_states():
    """show an HTML page
       get sorted states to add to an HTML UL tag.
       get ordered cities for each state into HTML file li Tag.
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('8-cities_by_states.html',
                           state_objs=state_objs)


@app.route('/states/<id>')
def html_if_stateID(id):
    """show the HTML page; use state.name to customize the heading
       pull sorted cities for state ID into the HTML file li Tag.
    """
    state_obj = None
    for state in storage.all("State").values():
        if state.id == id:
            state_obj = state
    return render_template('9-states.html',
                           state_obj=state_obj)


@app.route('/hbnb_filters')
def html_filters():
    """show HTML page with functional amenities, city and state filters
       use static CSS files for the web
    """
    state_objs = [s for s in storage.all("State").values()]
    amenity_objs = [a for a in storage.all("Amenity").values()]
    return render_template('10-hbnb_filters.html',
                           state_objs=state_objs, amenity_objs=amenity_objs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
