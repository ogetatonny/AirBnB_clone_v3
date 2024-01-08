#!/usr/bin/python3
"""
script starts Flask web app
    listen on port 5000 at 0.0.0.0
    routes: /:                    shows "Hello HBNB!"
            /hbnb:                shows "HBNB"
            /c/<text>:            shows "C" + text (replace "_" with " ")
            /python/<text>:       shows "Python" + text (default="is cool")
            /number/<n>:          shows "n is a number" only if int
            /number_template/<n>: show the HTML page if n is int
            /number_odd_or_even/<n>: show HTML page; show even and odd info
            /states_list & /states:  show HTML and state info from storage
            /cities_by_states:    show HTML and state, city relations
            /states/<id>:         show HTML and state, city given state id
            /hbnb_filters:        show HTML w/ working state, city filter
            /hbnb:                show HTML w/ oper attrib amenity filter
"""
from models import storage
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """shows the text"""
    return "Hello HBNB!"


"""
@app.route('/hbnb')
def hbnb():
    """ """
    return "HBNB"
"""


@app.route('/c/<text>')
def c_text(text):
    """shows the text given"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """shows the text given
       first route statement ensures it works for:
          curl -Ls 0.0.0.0:5000/python ; echo "" | cat -e
          curl -Ls 0.0.0.0:5000/python/ ; echo "" | cat -e
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def text_if_int(n):
    """shows text if int gievn"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>')
def html_if_int(n):
    """shows html page if int given
       place give int into the html template
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def html_odd_or_even(n):
    """shows html page if int given
       place given int for html template
       replaces text to show int is odd or even
    """
    odd_or_even = "even" if (n % 2 == 0) else "odd"
    return render_template('6-number_odd_or_even.html',
                           n=n, odd_or_even=odd_or_even)


@app.teardown_appcontext
def tear_down(self):
    """Remove current SQLAlchemy session after request."""
    storage.close()


@app.route('/states')
@app.route('/states_list')
def html_fetch_states():
    """shows html page
       get sorted states to add to an HTML UL tag.
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('7-states_list.html',
                           state_objs=state_objs)


@app.route('/cities_by_states')
def html_fetch_cities_by_states():
    """shows html page
       retrieve ordered states for the UL tag HTML insert.
       get ordered cities for state into HTML file LI tag.
    """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('8-cities_by_states.html',
                           state_objs=state_objs)


@app.route('/states/<id>')
def html_if_stateID(id):
    """show HTML page; use state.name to customize the heading
       pull sorted cities for state ID into HTML file LI tag
    """
    state_obj = None
    for state in storage.all("State").values():
        if state.id == id:
            state_obj = state
    return render_template('9-states.html',
                           state_obj=state_obj)


@app.route('/hbnb_filters')
def html_filters():
    """show HTML page with functional amenities and city, state filters
       use static CSS files for the web
    """
    state_objs = [s for s in storage.all("State").values()]
    amenity_objs = [a for a in storage.all("Amenity").values()]
    return render_template('10-hbnb_filters.html',
                           state_objs=state_objs, amenity_objs=amenity_objs)


@app.route('/hbnb')
def html_all_filters():
    """show an HTML page with functional city, state filters and properties
       use static CSS files for the web
    """
    state_objs = [s for s in storage.all("State").values()]
    amenity_objs = [a for a in storage.all("Amenity").values()]
    place_objs = [p for p in storage.all("Place").values()]
    user_objs = [u for u in storage.all("User").values()]
    place_owner_objs = []
    for place in place_objs:
        for user in user_objs:
            if place.user_id == user.id:
                place_owner_objs.append(["{} {}".format(
                    user.first_name, user.last_name), place])
    place_owner_objs.sort(key=lambda p: p[1].name)
    return render_template('100-hbnb.html',
                           state_objs=state_objs,
                           amenity_objs=amenity_objs,
                           place_owner_objs=place_owner_objs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
