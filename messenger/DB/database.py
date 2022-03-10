import psycopg2

con = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
print("Database opened successfully!")
cur = con.cursor()
cur.execute("select * from users")
for i in cur.fetchall():
    print(i)
con.commit()

con.close()