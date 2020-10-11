from flask import Flask
from flask_restplus import Resource
from flask_util import SecureApi
from os import path
from .patreon import fetch_patrons
import time


name = "Servey Patrons"
app = Flask(name)
api = SecureApi(app, doc="/")
api.title = name


directory = path.dirname(path.dirname(path.abspath(__file__)))
patrons_path = path.join(path.dirname(path.abspath(__file__)), "../patrons.csv")

whitelist = [  # Only report these fields
    "Name",
    "Twitter",
    "Patron Status",
    "Follows You",
    "Lifetime Amount",
    "Pledge Amount",
    "Charge Frequency",
    "Tier",
    "Patronage Since Date",
    "Last Charge Date",
    "Last Charge Status",
    "User ID",
    "Last Updated",
    ]

if not path.isfile(patrons_path):
    raise FileNotFoundError("Patrons CSV file not found!")

patrons = {"list": [], "updated": 0.0}


def get_patrons():
    # Cache patrons list for up to an hour, make a new API call once we go over that limit
    if patrons["updated"] + 3600 < time.time() or not patrons["list"]:
        print("Cache outdated, making a new Patreon API call!")
        patrons["list"] = fetch_patrons()
        patrons["updated"] = time.time()
    return patrons["list"]


@api.route("/patrons")
class PatronsList(Resource):
    # All patrons
    @staticmethod
    def get():
        return get_patrons()



@api.route("/patrons/sorted")
class PatronsListSorted(Resource):
    # Patrons sorted by lifetime pledge
    @staticmethod
    def get():
        return sorted(
            PatronsList(api=api).get(),
            key=lambda patron: patron["lifetime_amount"],
            reverse=True
        )


@api.route("/patron/<string:user_id>")
class PatronByName(Resource):
    # A singular patron
    @staticmethod
    def get(user_id: str):
        return patrons[user_id]


def main():
    app.run()


if __name__ == "__main__":
    main()
