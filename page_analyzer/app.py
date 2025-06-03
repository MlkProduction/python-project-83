import os
import requests


import psycopg2
import validators

from flask import Flask, render_template, request, flash, url_for, redirect, abort
from dotenv import load_dotenv
from datetime import datetime

from repository import UrlsRepository
from validator import validate

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
repo = UrlsRepository(conn)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def courses_index():

    return render_template(
        'index.html',
    )
# @app.route("/urls", methods=["GET"])
# def urls():
#     return render_template("index.html")
@app.route("/", methods=["POST", "GET"])
def urls_post():
    data = request.form.to_dict()

    errors = validate(data)

    if not errors:
        data["created_at"] = datetime.now()
        url_id = repo.create(data)
        
        flash('Urls has been checked', 'success')
        return redirect(url_for('urls_checks', id=url_id))
    else:
        flash(errors)

    return render_template("index.html", url=data, errors=errors), 422

@app.route("/urls/<int:id>")
def urls_showid(id):
    urls = repo.find(id)
    if urls is None:
        abort(404)
    return render_template("show.html", urls=urls)


@app.route("/urls")
def urls_show():
    all_urls = repo.all()
    if all_urls is None:
        abort(404)
    
    return render_template("showall.html", urls=all_urls)

@app.route("/urls/<int:id>/checks", methods=['POST', 'GET'])
def urls_checks(id):
    url_check = repo.find(id) #
    if url_check is None: #проверяем есть или нет такой id
        abort(404)

    response = requests.get(url_check['name'], timeout=5) #делаем запрос 
    response.raise_for_status() #запрос
    status_code = response.status_code #получаем статус кода

    check_data = {
    'url_id': id,
    'status_code': status_code, 
    'h1': '',
    'title': '',
    'description': '',
    'created_at': datetime.now()
    }
    
    print(check_data)
    repo.save_checks(check_data)
   
    
    return render_template("checks.html", url_check=url_check, check_data=check_data )



if __name__ == "__main__":
    app.run(debug=True)