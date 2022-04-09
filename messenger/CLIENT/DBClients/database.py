import sqlite3

# Connection:
def get_connection_sqlite():
    return sqlite3.connect('clients.db')


def close_connectin_sqlite(con):
    con.close()

