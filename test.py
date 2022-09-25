from ZODB import DB
import transaction


db = DB(None)
with db.transaction() as conn:
    conn.root.employees = ['Bill']
with db.transaction() as conn:
    print(conn.root)