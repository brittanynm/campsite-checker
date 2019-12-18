"""Final project: campsite checker"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Campsite, Request

import datetime
from lookup import is_valid_number
from api import check_availability, get_num_available_sites

app = Flask(__name__)

app.secret_key = "ABC"
app.jinja_env.undefined = StrictUndefined


@app.route("/", methods=["GET"])
def index():
    """Show homepage and campsite search"""
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
    campsites = (
        q.filter(
            (Campsite.name.ilike(f"%{campsite_name}%"))
            | (Campsite.park.ilike(f"%{campsite_name}%"))
        )
        .limit(100)
        .all()
    )
    results = {}
    for campsite in campsites:
        results[campsite.id] = {
            "name": campsite.name,
            "park": campsite.park,
            "id": campsite.id,
        }

    return jsonify(results)


@app.route("/dates", methods=["GET", "POST"])
def date_selector():
    """Collect check in and check out dates"""
    if request.method == "GET":
        campsite_name = request.args.get("query")
        return render_template("calendar.html")
    else:
        date_start = request.form["date-start"]
        dates = date_start.split(" - ")
        date_start = dates[0]
        date_end = dates[1]
        session["date_start"] = date_start
        session["date_end"] = date_end
        session["date_start_dt"] = datetime.datetime.strptime(date_start, "%m/%d/%Y")
        session["date_end_dt"] = datetime.datetime.strptime(date_end, "%m/%d/%Y")
        return redirect("/submit")


@app.route("/submit", methods=["GET", "POST"])
def submission_form():
    """Display previous selections, collect phone number, and commit to db"""
    if request.method == "GET":
        list_of_objs = []
        available_list = []
        avail_num = []
        totals = []
        for campsite in session["campsites"]:
            site_obj = Campsite.query.filter_by(id=campsite).one()
            list_of_objs.append(site_obj)
            resp = check_availability(
                session["date_start_dt"], session["date_end_dt"], campsite
            )
            available = get_num_available_sites(
                resp, session["date_start_dt"], session["date_end_dt"]
            )
            available_list.append(available)
            avail_num.append(available[0])
        for item in available_list:
            chars = item.split()
            totals.append(chars[5])

        return render_template(
            "submission_form.html",
            campsites=session["campsites"],
            list_of_objs=list_of_objs,
            date_start=session["date_start"],
            date_end=session["date_end"],
            available=available_list,
            avail_num=avail_num,
            totals=totals,
        )
    else:
        phone = request.form["phone"]
        valid = is_valid_number(phone)
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
                    date_start=session["date_start_dt"],
                    date_end=session["date_end_dt"],
                )
                db.session.add(new_request)
                # convert campsite list to set before comitting to db
                db.session.commit()
                # clear individual keys for session
            return render_template("confirm.html")


@app.route("/validate-phone-number.json", methods=["GET"])
def validate_phone_number():

    phone = request.args["phone"]

    return jsonify({"is_valid": is_valid_number(phone)})


@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    # Change to False for demo
    app.debug = False
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
