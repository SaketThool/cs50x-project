import csv
from pprint import pprint
from flask import Flask, render_template

# Configure application
app = Flask(__name__)


def load_data():
    with open("data/worldcups.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

@app.route("/")

def index():
    cups = load_data()
    # pprint(cups)
    return render_template("index.html", cups=cups)

@app.route("/year/<int:year>")
def details(year):
    # pprint(year)
    cups = load_data()
    cup = None
    for c in cups:
        if int(c["year"]) == year:
            cup = c
            break
    return render_template("details.html", cup=cup)