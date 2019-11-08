"""Final project: campsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request

from flask_wtf import Form
from wtforms import DateField
from datetime import date
# import api

app = Flask(__name__)

app.secret_key = 'ABC'

# Raises an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Show homepage and form for campsite search"""
    campsites = Campsite.query.all()

    return render_template("homepage.html", campsites=campsites)


@app.route('/search')
def search():
    """Process campsite search"""

    # Get form variable
    campsite_name = request.args.get("query")
    # Search database by name and park
    q = Campsite.query
    campsites = q.filter( (Campsite.name.ilike(f'%{campsite_name}%')) | (Campsite.park.ilike(f'%{campsite_name}%'))).all()
    campsites = campsites

    return render_template("homepage.html", campsites=campsites)
    

@app.route('/search', methods=['POST'])
def process_search():
    # WIP
    selected_campsite = request.form["selected_site"]
    print(selected_campsite)
    #add selection to URL
    return redirect("/dates")


# @app.route('/dates', methods=['GET'])
# # should I store campsite in URL?
# def date_selector():
#     """Show calendar to select check in, check out dates"""

#     return render_template("calendar.html")

class DateForm(Form):
    dt = DateField('Pick a Date', format="%m/%d/%Y")


@app.route('/dates', methods=['POST','GET'])
def home():
    form = DateForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%x')
    return render_template('calendar.html', form=form)





@app.route('/dates', methods=['POST'])
def process_dates(start, end):
    """Process dates selected"""

    # Get form variables
    date_start = request.form["date_start"]
    date_end = request.form["date_end"]

    # date_obj = 

    # current_date = get today's datetime
    valid_date(date_obj)

    return redirect("/submit")


@app.route('/submit', methods=['GET'])
# should I store previous selections in URL?
def submission_form():
    """Collect phone number and display previous selections"""

    #additionally display current availability

    return render_template("submission_form.html")


@app.route('/submit', methods=['POST'])
def process_request():
    """Process request for campsite notification"""

    # Get form variables
    phone = request.form["phone"]
    #validate phone with regex in jinja and here

    #created_at = get today's datetime

    return render_template("confirmation_page.html")


if __name__ == "__main__":

    # Change to False for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")