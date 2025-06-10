import psycopg2
from psycopg2.extras import DictCursor

class UrlsRepository:
    def __init__(self, dsn):
        self.dsn = dsn

    def get_connection(self):
        return psycopg2.connect(self.dsn)

    def create(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO urls (name, created_at) 
                    VALUES (%s, CURRENT_DATE)
                    RETURNING id;
                    """,
                    (url['url'],)
                )
                url_id = cur.fetchone()[0]
                url['id'] = url_id
            conn.commit()
            return url_id
    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls ORDER BY id DESC")
                return cur.fetchall()

    def find_url(self, name):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
                row = cur.fetchone()
                return dict(row) if row else None

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def all(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
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

    def save_checks(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        url['url_id'],
                        url['status_code'],
                        url['h1'],
                        url['title'],
                        url['description'],
                        url['created_at']
                    )
                )
                check_id = cur.fetchone()[0]
            conn.commit()
            return check_id

    def get_checks(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM url_checks WHERE url_id = %s", (url_id,))
                row = cur.fetchone()
                return dict(row) if row else None
