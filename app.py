from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://127.0.0.1:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_facts

# mongo = pymongo(app, uri="mongodb://127.0.0.1.27017/mars_app")

@app.route("/")

def home():
    mars = list(db.mars_facts.find())
    print(mars)
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    db.mars_facts.insert_one(mars_data)
    # mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
