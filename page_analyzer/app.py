import os
from urllib.parse import urlparse

import requests
import psycopg2

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, flash, url_for, redirect, abort
from dotenv import load_dotenv
from datetime import datetime


from page_analyzer.repository import UrlsRepository
from page_analyzer.validator import validate
# from repository import UrlsRepository
# from validator import validate

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

repo = UrlsRepository(app.config['DATABASE_URL'])


def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    return f"{scheme}://{netloc}"


@app.route('/')
def index():
    # messages = get_flashed_messages(with_categories=True)
    # return render_template('index.html', messages=messages, url='')
    return render_template('index.html', url='')
@app.route("/urls", methods=["GET", "POST"])
def urls_post():
    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate(data)
        url_name = data.get('url')
        urls = repo.get_content()
        existing_url = repo.find_url(url_name)
        # normal_url = normalize_url(existing_url['name'])
        
        all_url = []
        for url in urls:
            all_url.append(url['name'])
            
        data['url'] = normalize_url(data['url'])
        if data['url'] in all_url:
                flash('Страница уже существует', 'danger')
                id = repo.find_url(data['url'])['id']
                return redirect(url_for('urls_showid', id=id))
        
        if not existing_url and not errors:
            data["created_at"] = datetime.now()
            url_id = repo.create(data)
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('urls_showid', id=url_id))


        if errors:
            flash(errors, 'danger')  
            return render_template("index.html", url=data, errors=errors), 422

    return render_template("index.html", url={}, errors={})

@app.route("/urls/<int:id>")
def urls_showid(id):
    urls = repo.find(id)
    if urls is None:
        abort(404)
    checks = repo.get_checks(id)
    return render_template("url.html", urls=urls, checks=checks)


@app.route("/urls")
def urls_show():
    all_urls = repo.all()
    if all_urls is None:
        abort(404)
    return render_template("urls.html", urls=all_urls)

@app.route("/urls/<int:id>/checks", methods=['POST'])
def urls_checks(id):
    url_check = repo.find(id) #
    if url_check is None: #проверяем есть или нет такой id
        abort(404)
        
    try:
        r = requests.get(url_check['name'], timeout=10) #делаем запрос 
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('urls_showid', id=id))
    
    status_code = r.status_code
    soup = BeautifulSoup(r.text, 'html.parser')
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