import psycopg2

def get_connection():
    return psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
print("Database opened successfully!")
def close_connectin(con):
    con.close()