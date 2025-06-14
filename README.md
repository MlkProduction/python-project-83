### Hexlet tests and linter status:
[![Actions Status](https://github.com/MlkProduction/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MlkProduction/python-project-83/actions)

### Sonar Cloud status:
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MlkProduction_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=MlkProduction_python-project-83)

# 📊 Анализатор страниц

🔗 [Демо на Render](https://python-project-83-x0to.onrender.com/)

---

## 📝 Описание

**Анализатор страниц** — веб-приложение для проверки сайтов на базовые SEO-параметры. Оно позволяет пользователю отправить URL и получить информацию о заголовке страницы (`<title>`), заголовке первого уровня (`<h1>`) и meta-описании.

---

## ⚙️ Технологии

| Технология | Описание |
|------------|----------|
| [Flask](https://flask.palletsprojects.com/) | Фреймворк для создания веб-приложений |
| [Gunicorn](https://gunicorn.org/) | WSGI-сервер для продакшн |
| [Requests](https://requests.readthedocs.io/) | Библиотека для HTTP-запросов |
| [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) | HTML-парсер |
| [PostgreSQL](https://www.postgresql.org/) + [psycopg2](https://www.psycopg.org/) | База данных |
| [Ruff](https://docs.astral.sh/ruff/) | Линтер и автоформаттер |
| [Bootstrap](https://getbootstrap.com/) | Стилизация интерфейса |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Загрузка переменных из `.env` |

---

## 🚀 Установка и запуск

```bash
git clone git@github.com:MlkProduction/python-project-83.git
cd python-project-83
Укажи свои значения переменных: DATABASE_URL, SECRET_KEY и т.д. в .env

make build     # установка зависимостей
make start     # запуск сервера


Site is available [here](https://python-project-83-x0to.onrender.com/)