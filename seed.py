import requests
import json
import csv

from sqlalchemy import func
from model import User, Campsite, Request, connect_to_db, db
from server import app


def load_campsites():
    print("Campsites")

    for row in open("seed.csv", encoding="cp1252"):
        row = row.rstrip()
        site_id, name, park = row.split(",")
        site_id = site_id.title()
        name = name.title()
        park = park.title()

        campsite = Campsite(id=site_id, name=name, park=park)

        db.session.add(campsite)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_campsites()
