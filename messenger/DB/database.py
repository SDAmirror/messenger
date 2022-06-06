import psycopg2

# pool = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
def get_connection():
    return psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")

def close_connectin(con):
    con.close()