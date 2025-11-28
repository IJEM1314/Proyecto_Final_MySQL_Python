from db.db_connection import get_conn

def run_schema():
    conn = get_conn()
    cur = conn.cursor()

    with open("src/db/schema.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    for statement in sql.split(";"):
        stmt = statement.strip()
        if stmt:
            cur.execute(stmt)
    conn.commit()
    cur.close()
    conn.close()
    print("TABLAS CREADAS EXITOSAMENTE, SI NO SE VE ESTE MENSAJE ES PORQUE ALGO ESCRIBÍ MAL")

if __name__ == "__main__":
    run_schema()
