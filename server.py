"""Final project: campsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request

from flask_wtf import Form
from wtforms import DateField
from datetime import date
from lookup import is_valid_number
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Process campsite search"""
    if request.method == 'GET':
        # Get form variable
        campsite_name = request.args.get("query")
        # Search database by name and park
        q = Campsite.query
        campsites = q.filter( (Campsite.name.ilike(f'%{campsite_name}%')) | (Campsite.park.ilike(f'%{campsite_name}%'))).all()
        campsites = campsites
        return render_template("homepage.html", campsites=campsites)
    else:
        selected_site = request.form["selected_site"]
        session["site_name"] = selected_site
        #query db for campsite_id and set into session
        site_obj = Campsite.query.filter_by(name = selected_site).one()
        site_id = site_obj.id
        session["site_id"] = site_id
        

    return redirect("/dates")


@app.route('/dates', methods=['GET', 'POST'])
def process_dates():
    """Process dates selected"""
    if request.method == 'GET':
        campsite_name = request.args.get("query")
        return render_template("calendar.html", site_name=session['site_name'])
    else:
    # Get form variables
        date_start = request.form["date-start"]
        date_end = request.form["date-end"]
        session["date_start"] = date_start
        session["date_end"] = date_end

        return redirect("/submit")


@app.route('/submit', methods=['GET'])
# should I store previous selections in URL?
def submission_form():
    """Collect phone number and display previous selections"""

    #additionally display current availability

    return render_template("submission_form.html", 
                            site_name=session['site_name'],
                            date_start=session["date_start"], 
                            date_end=session["date_end"])


@app.route('/submit', methods=['POST'])
def process_request():
    """Process request for campsite notification"""
    # Get form variables
    phone = request.form["phone"]
    #instantiate a new User object that creates a Request and commits dates, campsite name, campsite ID
    #use session user_id to add to the request row
    if is_valid_number(phone) == True:
        print("**", phone)
        new_user = User(phone=phone)
        print("***", new_user)
        db.session.add(new_user)
        db.session.commit()
        test = new_user.user_id
        
        session["user_id"] = test
        
        new_request = Request(user_id=session["user_id"], campsite_id=session["site_id"], date_start=session["date_start"], date_end=session["date_end"])
        db.session.add(new_request)
        db.session.commit()

        return redirect("/")
    else:
        print("Invalid number")
        # block form from submitting in js
        flash("Please enter a valid phone number")
        return redirect("/")
    # or validate phone with regex in jinja and here
    

if __name__ == "__main__":

    # Change to False for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")