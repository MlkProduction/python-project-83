import os
import requests
import psycopg2

from bs4 import BeautifulSoup
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


@app.route("/", methods=["GET", "POST"])
def urls_post():
    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate(data)
        url_name = data.get('url')
        existing_url = repo.find_url(url_name)

        if existing_url:
            flash('Этот сайт уже проверяли', 'danger')
            return redirect(url_for('urls_show', errors={}))
        if not errors:
            data["created_at"] = datetime.now()
            url_id = repo.create(data)
            flash('URL успешно добавлен', 'success')
            return redirect(url_for('urls_showid', id=url_id))

        flash(errors, 'danger')
        return render_template("index.html", url=data, errors=errors), 422


    return render_template("index.html", url={}, errors={})

@app.route("/urls/<int:id>")
def urls_showid(id):
    urls = repo.find(id)
    if urls is None:
        abort(404)
    checks = repo.get_checks(id)
    return render_template("show.html", urls=urls, checks=checks)


@app.route("/urls")
def urls_show():
    all_urls = repo.all()
    if all_urls is None:
        abort(404)
    return render_template("showall.html", urls=all_urls)

@app.route("/urls/<int:id>/checks", methods=['POST'])
def urls_checks(id):
    url_check = repo.find(id) #
    if url_check is None: #проверяем есть или нет такой id
        abort(404)

    response = requests.get(url_check['name'], timeout=5) #делаем запрос 
    response.raise_for_status() #запрос
    status_code = response.status_code #получаем статус кода
    
    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.h1.text.strip() if soup.h1 else ''
    title = soup.title.text.strip() if soup.title else ''
    desc = soup.find('meta', attrs={'name': 'description'})
    description = desc['content'].strip() if desc and desc.get('content') else ''
    
    check_data = {
    'url_id': id,
    'status_code': status_code, 
    'h1': h1,
    'title': title,
    'description': description,
    'created_at': datetime.now()
    }
    repo.save_checks(check_data)
   
    return redirect(url_for('urls_showid', id=id))



if __name__ == "__main__":
    app.run(debug=True)