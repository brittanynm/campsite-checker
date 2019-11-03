"""Final project -- capsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar. Where does this password come from??
app.secret_key = "ABC"

# Raises an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/', methods=['GET'])
def campsite_search():
    """Show form for campsite search"""

    return render_template("campsite_search.html")


@app.route('/', methods=['POST'])
def process_search():
    """Process campsite search and selection"""

    # Get form variables
    selected_campsite = request.form["selected_campsite"]

    # How can I package all of this info at the end when phone is submitted?
    campsite = Request(selected_campsite=name)
    # Use selected campsite to look up campsite ID and store in DB

    db.session.add(campsite)
    db.session.commit()
    
    return redirect(f"/dates")


@app.route('/dates', methods=['GET'])
# should I store campsite in URL?
def date_selector():
    """Show calendar to select check in, check out dates"""

    return render_template("calendar.html")


@app.route('/dates', methods=['POST'])
def process_dates():
    """Process dates selected"""

    # Get form variables
   	date_start = request.form["date_start"]
    date_end = request.form["date_end"]

    # current_date = get today's datetime

    #if current_date > date_start:
        flash("Select a date in the future")

    return redirect(f"/submit")


@app.route('/submit', methods=['GET'])
# should I store previous selections in URL?
def submission_form():
    """Collect phone number and display previous selections"""

    return render_template("submission_form.html")


@app.route('/submit', methods=['POST'])
def process_request():
    """Process request for campsite notification"""

    # Get form variables
   	phone = request.form["phone"]

    #created_at = get today's datetime

    return redirect(f"/confirmation")


@app.route('/confirmation', methods=['GET'])
# should I store previous selections in URL?
def confirmation():
    """Confirm submitted information"""

    return render_template("confirmation_page.html")

