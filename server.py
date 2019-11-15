"""Final project: campsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request

from flask_wtf import Form
from datetime import date
from lookup import is_valid_number
from api import check_availability, get_num_available_sites
from schedule_check import *
import schedule

app = Flask(__name__)

app.secret_key = 'ABC'
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """Show homepage and campsite search"""
    campsites = Campsite.query.all()

    return render_template("homepage.html", campsites=campsites)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Filter search and process selection"""
    if request.method == 'GET':
        campsite_name = request.args.get("query")
        q = Campsite.query
        campsites = q.filter( (Campsite.name.ilike(f'%{campsite_name}%')) | (Campsite.park.ilike(f'%{campsite_name}%'))).all()
        return render_template("homepage.html", campsites=campsites)
    else:
        selected_site = request.form["selected_site"]
        session["site_id"] = selected_site
        site_obj = Campsite.query.filter_by(id = selected_site).one()
        site_name = site_obj.name
        session["site_name"] = site_name
        park_name = site_obj.park
        session["park_name"] = park_name
    
    return redirect("/dates")


@app.route('/dates', methods=['GET', 'POST'])
def process_dates():
    """Collect check in and check out dates"""
    if request.method == 'GET':
        campsite_name = request.args.get("query")
        return render_template("calendar.html", 
                                site_name=session["site_name"], 
                                park_name=session["park_name"])
    else:
        date_start = request.form["date-start"]
        date_end = request.form["date-end"]
        session["date_start"] = date_start
        session["date_end"] = date_end

        return redirect("/submit")


@app.route('/submit', methods=['GET', 'POST'])
def submission_form():
    """Display previous selections, collect phone number, and commit to db"""
    if request.method == 'GET':
        resp = check_availability(session["date_start"], session["date_end"], session["site_id"])
        available = get_num_available_sites(resp, session["date_start"], session["date_end"])
        print(available)
        return render_template("submission_form.html", 
                            site_name=session['site_name'],
                            date_start=session["date_start"], 
                            date_end=session["date_end"],
                            available=available)
    else:
        phone = request.form["phone"]
        if is_valid_number(phone) == True:
            new_user = User(phone=phone)
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id
            session["user_id"] = user_id
            new_request = Request(user_id=session["user_id"], campsite_id=session["site_id"], date_start=session["date_start"], date_end=session["date_end"])
            db.session.add(new_request)
            db.session.commit()
            return redirect("/")
        else:
            print("Invalid number")
            # block form from submitting in js
            flash("Please enter a valid phone number")
            return redirect("/")
    

if __name__ == "__main__":
    # Change to False for demo
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    schedule.run_pending() 
    app.run(host="0.0.0.0")
