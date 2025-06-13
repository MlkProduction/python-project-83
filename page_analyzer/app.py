import os
from urllib.parse import urlparse

import requests


from bs4 import BeautifulSoup
from flask import (
    Flask,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    abort,
    get_flashed_messages,
)
from dotenv import load_dotenv
from datetime import datetime


from page_analyzer.repository import UrlsRepository
from page_analyzer.validator import validate


load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")

repo = UrlsRepository(app.config["DATABASE_URL"])


def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    return f"{scheme}://{netloc}"


@app.route("/")
def index():

    return render_template("index.html", url="")


@app.route("/urls", methods=["POST"])
def urls_post():
    data = request.form.to_dict()
    errors = validate(data)
    url_name = data.get("url")
    urls = repo.get_content()
    existing_url = repo.find_url(url_name)
    all_url = []
    
    for url in urls:
        all_url.append(url["name"])

    data["url"] = normalize_url(data["url"])
    if data["url"] in all_url:
        flash("Страница уже существует", "danger")
        id = repo.find_url(data["url"])["id"]
        return redirect(url_for("urls_showid", id=id))

    if not existing_url and not errors:
        data["created_at"] = datetime.now()
        url_id = repo.create(data)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("urls_showid", id=url_id))

    if errors:
        flash(errors, "danger")
        return render_template("index.html", url=data, errors=errors), 422
    return render_template("index.html", url={}, errors={})


@app.route("/urls/<int:id>")
def urls_showid(id):
    urls = repo.find(id)
    messages = get_flashed_messages(with_categories=True)
    checks = repo.get_checks(id)
    return render_template("url.html", urls=urls, checks=checks, 
                           messages=messages)


@app.route("/urls")
def urls_get():
    all_urls = repo.all()
    if all_urls is None:
        abort(404)
    return render_template("urls.html", urls=all_urls)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def urls_checks(id):
    url_check = repo.find(id)  #
    url = url_check["name"]

    try:
        r = requests.get(url, timeout=10)  # делаем запрос
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for("urls_showid", id=id))

    status_code = r.status_code
    if str(status_code)[0] in ("4", "5"):
        flash("Произошла ошибка при проверке", "alert-danger")
        return redirect(url_for("urls_showid", id=id))

    soup = BeautifulSoup(r.text, "html.parser")
    h1 = soup.h1.text.strip() if soup.h1 else ""

    title = soup.title.text.strip() if soup.title else ""

    desc = soup.find("meta", attrs={"name": "description"})

    description = desc["content"].strip() \
        if desc and desc.get("content") else ""

    check_data = {
        "url_id": id,
        "status_code": status_code,
        "h1": h1,
        "title": title,
        "description": description,
        "created_at": datetime.now(),
    }
    repo.save_checks(check_data)

    flash("Страница успешно проверена", "success")
    return redirect(url_for("urls_showid", id=id))


if __name__ == "__main__":
    app.run(debug=True)
