from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import Scrape_Mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

@app.route('/')

def home():

    # Find one record of data from the mongo database
    Mars = mongo.db.Mars.find_one()

    # Return template and data
    return render_template("index.html", Mars=Mars)


@app.route('/scrape')
def scrape():
    scraped_data = Scrape_Mars.scrape()

    mongo.db.Mars.update({},scraped_data,upsert = True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug = True)