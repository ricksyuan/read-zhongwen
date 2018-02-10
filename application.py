#!flask/bin/python

import re
import sqlite3

from tictoc import TicToc
from lookup import lookup
from searchesdb import searchSucceeded, insertSearch, searchFailed


from flask import Flask, flash, redirect, render_template, request, session, url_for
from flaskrun import flaskrun


application = Flask(__name__)

# configure application

# ensure responses aren't cached
if application.config["DEBUG"]:
    @application.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@application.route("/", methods=["GET"])
def index():
    """Main page"""
    if request.method == "GET":
        return render_template("index.html")
        
@application.route("/read", methods=["GET", "POST"])
def read():
    """Display augmented Chinese characters for reading."""
    if request.method == "GET":
        return redirect(url_for("index"))
    if request.method == "POST":
        # begin timing how long it takes to load the CEDICT dictionary
        timer = TicToc()
        
        text = request.form["pastedtext"]
        
        # add input text to search database, store search id for later updates,
        search_id = insertSearch(text[0:1000]) # Limit search added to database to 1000 characters to prevent size from growing too large
        # update database that search was not successful
        if len(text) > 1000:
            searchFailed(search_id, "Input exceeded length limit")
            # notify user
            return render_template("checkinput.html")
        (phrases, mode) = lookup(text)
        elapsed_time = timer.toc("Returning phrases")
        character_count = 0
        phrase_count = 0
        
        
        
        for phrase in phrases:
            if phrase["definitions"] != None:
                phrase_count += 1    
            characters = phrase['lookup']
            character_count += len(characters)
        
        # update database that search was successful
        searchSucceeded(search_id, mode)
        
        # return page to user
        return render_template("read.html", phrases=phrases, elapsed_time=elapsed_time, character_count=character_count, phrase_count=phrase_count)
        
@application.route("/about", methods=["GET"])
def about():
    """About page"""
    if request.method == "GET":
        phrases = lookup("读中文")
        return render_template("about.html", phrases=phrases)
        
        
if __name__ == '__main__':
    flaskrun(application)