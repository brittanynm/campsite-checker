"""Final project: campsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request

from flask_wtf import Form
from datetime import date
from lookup import is_valid_number
from api import check_availability, get_num_available_sites

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route("/", methods=["GET"])
def index():
    """Show homepage and campsite search"""
    # campsites = Campsite.query.filter(Campsite.park.ilike('Yosemite')).all()
    campsites = Campsite.query.all()
    return render_template("homepage.html", campsites=campsites)


@app.route("/search", methods=["GET", "POST"])
def search():
    """Filter search and process selection"""
    if request.method == "GET":
        campsite_name = request.args.get("query")
        q = Campsite.query
        campsites = q.filter(
            (Campsite.name.ilike(f"%{campsite_name}%"))
            | (Campsite.park.ilike(f"%{campsite_name}%"))
        ).all()
        return render_template("homepage.html", campsites=campsites)
    else:
        site_list = request.form.getlist("selected_site")
        session["campsites"] = site_list

    return redirect("/dates")


@app.route("/live_search", methods=["GET"])
def live_search():
    campsite_name = request.args.get("query")
    q = Campsite.query
    campsites = q.filter(
        (Campsite.name.ilike(f"%{campsite_name}%"))
        | (Campsite.park.ilike(f"%{campsite_name}%"))
        ).all()
    results = {}
    for campsite in campsites:
        results[campsite.id] = {'name': campsite.name, 'park':campsite.park, 'id':campsite.id}

    return jsonify(results)

# @app.route("/original_display", methods=["GET"])
# def original_display():
#     q = Campsite.query
#     campsites = q.filter(
#         (Campsite.park.ilike("yosemite"))
#         ).all()

#     results = {}
#     for campsite in campsites:
#         results[campsite.id] = {'name': campsite.name, 'park':campsite.park, 'id':campsite.id}

#     return jsonify(results)


@app.route("/dates", methods=["GET", "POST"])
def date_selector():
    """Collect check in and check out dates"""
    if request.method == "GET":
        campsite_name = request.args.get("query")
        return render_template(
            "calendar.html"
        )
    else:
        date_start = request.form["date-start"]
        date_end = request.form["date-end"]
        session["date_start"] = date_start
        session["date_end"] = date_end

        return redirect("/submit")


@app.route("/submit", methods=["GET", "POST"])
def submission_form():
    """Display previous selections, collect phone number, and commit to db"""
    if request.method == "GET":
        list_of_objs = []
        available_list = []
        for campsite in session["campsites"]:
            site_obj = Campsite.query.filter_by(id=campsite).one()
            list_of_objs.append(site_obj)
            resp = check_availability(
                session["date_start"], session["date_end"], campsite
            )
            available = get_num_available_sites(
                resp, session["date_start"], session["date_end"]
            )
            available_list.append(available)
        
        return render_template(
            "submission_form.html",
            campsites=session["campsites"],
            list_of_objs=list_of_objs,
            date_start=session["date_start"],
            date_end=session["date_end"],
            available=available_list
        )
    else:
        phone = request.form["phone"]
        if is_valid_number(phone) is True:
            new_user = User(phone=phone)
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id
            session["user_id"] = user_id
            for site in session["campsites"]:
                new_request = Request(
                    user_id=session["user_id"],
                    campsite_id=site,
                    date_start=session["date_start"],
                    date_end=session["date_end"],
                )
                db.session.add(new_request)
                #convert campsite list to set before comitting to db
                db.session.commit()
                # clear individual keys for session
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
    app.run(host="0.0.0.0")
