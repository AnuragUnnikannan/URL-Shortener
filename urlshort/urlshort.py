from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os
from werkzeug.utils import secure_filename

bp = Blueprint("urlshort", __name__)

@bp.route("/")
def home():
    return render_template("index.html", codes=session.keys())

def storeURLInFile(code, url='', filename=''):
    temp = {}
    if os.path.exists("urls.json"):
        with open("urls.json") as file:
            temp = json.load(file)
            print(temp)
    
    if code in temp:
        flash("This short name already exists")
        return False
    else:
        urls = {}

        if filename == '':
            urls[code] = {"url":url}
        elif url == '':
            urls[code] = {"file":filename}
        
        temp = list(temp.items())
        urls = list(urls.items())
        temp.extend(urls)
        temp = dict(temp)
        with open("urls.json", "w") as file:
            json.dump(temp, file)
            session[code] = True
        
        return True
        

@bp.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        code = ''
        res = ''
        if "url" in request.form.keys():
            code = request.form["code"]
            res = storeURLInFile(code, url=request.form["url"])
        else:
            f = request.files["file"]
            code = request.form["code"]
            filename = code + secure_filename(f.filename)
            f.save("static/user_files/"+filename)
            res = storeURLInFile(code, filename=filename)

        if res:
            return render_template("index.html", url="127.0.0.1:5000/"+code, codes=session.keys())
        else:
            return redirect(url_for('urlshort.home'))

    else:
        return redirect(url_for("urlshort.home"))

@bp.route("/<string:code>")
def gotourl(code):
    if os.path.exists("urls.json"):
        with open("urls.json") as file:
            temp = json.load(file)
            if code in temp:
                if "url" in temp[code]:
                    return redirect(temp[code]["url"])
                else:
                    return redirect(url_for("static", filename="user_files/"+temp[code]["file"]))
    
    return abort(404)

@bp.errorhandler(404)
def pageNotFound(error):
    return render_template("page_not_found.html"), 404

@bp.route("/api")
def session_api():
    return jsonify(list(session.keys()))