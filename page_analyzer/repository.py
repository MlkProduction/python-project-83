import psycopg2
from psycopg2.extras import DictCursor


class UrlsRepository:
    def __init__(self, conn):
        self.conn = conn
    # 
    # def get_content(self):
    #     with self.conn.cursor(cursor_factory=DictCursor) as cur:
    #         cur.execute("SELECT * FROM urls")
    #         return [dict(row) for row in cur]
    # 
    # def find(self, id):
    #     with self.conn.cursor(cursor_factory=DictCursor) as cur:
    #         cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
    #         row = cur.fetchone()
    #         return dict(row) if row else None
    # 
    # def get_by_term(self, search_term=""):
    #     with self.conn.cursor(cursor_factory=DictCursor) as cur:
    #         cur.execute(
    #             """
    #                 SELECT * FROM cars
    #                 WHERE manufacturer ILIKE %s OR model ILIKE %s
    #             """,
    #             (f"%{search_term}%", f"%{search_term}%"),
    #         )
    #         return cur.fetchall()
    # 
    # def save(self, car):
    #     if "id" in car and car["id"]:
    #         self._update(car)
    #     else:
    #         self._create(car)
    # 
    # def _update(self, car):
    #     with self.conn.cursor() as cur:
    #         cur.execute(
    #             "UPDATE cars SET manufacturer = %s, model = %s WHERE id = %s",
    #             (car["manufacturer"], car["model"], car["id"]),
    #         )
    #     self.conn.commit()

    def create(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (url['url'], url['created_at']))
            url_id = cur.fetchone()[0]
            self.conn.commit()
            return url_id
        
    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def all(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY id")
            rows = cur.fetchall()
            return [dict(row) for row in rows]