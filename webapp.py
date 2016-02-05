#!/usr/bin/python3

from flask import Flask, jsonify
from music_finder import check_in_db, fetch_links

app = Flask(__name__)

@app.route("/")
def usage():
    return "Try with /search/MyQuery"

@app.route("/search/<query>")
def search(query):
    result, success = check_in_db(query)
    if success is True:
        return jsonify(result)
    return "Not found"

@app.route("/fetch/<query>")
def fetch(query):
    success, value = fetch_links(query)
    return value

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',"Origin, X-Requested-With, Content-Type, Accept")
    response.headers.add('Content-Type','application/json')
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
