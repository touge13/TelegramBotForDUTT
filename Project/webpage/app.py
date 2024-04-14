from flask import Flask, render_template, request
import os
import urllib.parse as up
import psycopg2


app = Flask(__name__)

up.uses_netloc.append("postgres")
key = os.environ.get('pswrd')
conn = psycopg2.connect(f"dbname='rahycxvn' user='rahycxvn' host='hattie.db.elephantsql.com' password={key}")
cur = conn.cursor()

@app.route("/")  
def index():  
    return render_template("index.html"); 
 
 
@app.route("/view")  
def view():  
    global cur

    cur.execute("SELECT * FROM survey")  
    rows = cur.fetchall()  
    conn.commit()

    cur.execute("SELECT grade FROM survey")
    users_list = []
    massive_big = cur.fetchall()
    for row in massive_big:
        for x in row:
            users_list.append(int(x))
    sur1 = sum(users_list)/len(users_list)
    sur = round(sur1, 1)
    return render_template("view.html", rows = rows, sur=sur)
 
    
if __name__ == '__main__':
   app.run(debug = True)
