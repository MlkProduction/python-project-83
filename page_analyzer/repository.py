import psycopg2
from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn
    #добавляем урлки в базу
    def create(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (url['url'], url['created_at']))
            url_id = cur.fetchone()[0]
            self.conn.commit()
            return url_id
        
    def find_url(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
            row = cur.fetchone()
            return dict(row) if row else None

    # ищем урлки в базе
    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    # выводим все урлки из базы
    def all(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT DISTINCT ON (u.id)
                    u.id, u.name, u.created_at,
                    c.status_code, c.created_at AS check_created_at
                FROM urls u
                LEFT JOIN url_checks c ON u.id = c.url_id
                ORDER BY u.id, c.created_at DESC;
            """)
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    # добавляем проверку сайта
    def save_checks(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                (url['url_id'], url['status_code'], url['h1'], url['title'], url['description'], url['created_at']))
            url_id = cur.fetchone()[0]
            self.conn.commit()
            return url_id

    # вынимаем проверку сайта
    def get_checks(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s", (url_id,))
            row = cur.fetchone()
            return dict(row) if row else None