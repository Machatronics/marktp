import sqlite3 as sql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
from flask import Flask,render_template,request
from billetspython import data_id_val,price_db,value,needle_size_db,composition_db
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/addnew')
def new_civilization():
    return render_template('billets.html')

@app.route("/addrec",methods = ['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                composition = request.form['composition']
                if id == "" or composition == "" :
                    msg = "id or composition can't be empty"
                    return render_template('result.html')
                cur = con.cursor()
                cur.execute("")
                cur.execute("INSERT INTO Billets VALUES (:DataId,:price,:delivery_time,:needle_size,:composition)",(data_id_val,price_db,value,needle_size_db,composition_db))
                con.commit()
                msg = "Success"
        except :
            con.rollback()
            msg = "Error"
        finally:
            con.close()
            return render_template('result.html',msg = msg)
@app.route('/list')
def list():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Billets")
    rows = cur.fetchall()
    return render_template("list.html", rows = rows)

@app.route('/d_specify')
def d_specify():
    return render_template('remove.html')

@app.route('/d_ specific', methods = ['POST','GET'])
def d_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                cur = con.cursor()
                field = request.form.get('options')
                if field == "id":
                    id = request.form['inputted']
                    form_selected = int(id)
                    cur.execute("DELETE FROM Billets WHERE DataId = ?",(form_selected,))
                elif field == "price":
                    price = request.form['inputted']
                    form_selected = price
                    cur.execute("DELETE FROM Billets WHERE price = ?",(form_selected,))
                elif field == "delivery_time":
                    delivery_time = request.form['inputted']
                    form_selected = delivery_time
                    cur.execute("DELETE FROM Billets WHERE delivery_time = ?",(form_selected,))
                elif field == "needle_size":
                    needle_size = request.form['inputted']
                    form_selected = needle_size
                    cur.execute("DELETE FROM Billets WHERE needle_size = ?",(form_selected,))
                elif field == "composition":
                    composition = request.form['inputted']
                    form_selected = composition
                    cur.execute("DELETE FROM Billets WHERE composition = ?",(form_selected,))
                
                con.commit()
                msg = "success"
        except:
            con.rollback()
            msg = "Error"
        finally:
            con.close()
            return render_template('result.html', msg = msg)

@app.route('/u_specify')
def u_specify():
    return render_template('update.html')

@app.route("/u_specific", methods = ['POST','GET'])
def u_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                field = request.form.get('options')
                id = int(request.form['id'])
                if field == "price":
                    price = request.form['inputted']
                    form_selected = price
                    cur.execute("UPDATE Billets SET price=? WHERE DataId=?", (form_selected,id))
                elif field == "delivery_time":
                    delivery_time = request.form['inputted']
                    form_selected = delivery_time
                    cur.execute("UPDATE Billets SET delivery_time=? WHERE DataId=?", (form_selected, id))
                elif field == "needle_size":
                    needle_size = request.form['inputted']
                    form_selected = needle_size
                    cur.execute("UPDATE Billets SET needle_size=? WHERE DataId=?", (form_selected, id))
                elif field == "composition":
                    composition = request.form['inputted']
                    form_selected = composition
                    cur.execute("UPDATE Billets SET composition=? WHERE DataId=?", (form_selected, id))
                con.commit()
                msg = "Successfully updated."
        except:
            msg = "Update failed."
            con.rollback()
        finally:
            con.close()
            return render_template('result.html', msg=msg)
@app.route('/s_specify')
def s_specify():
    return render_template('select.html')

@app.route('/s_specific', methods=['POST', 'GET'])
def s_specific():
    if request.method == 'POST':
        try:
            with sql.connect('database.db') as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                field = request.form.get('options')
                selected_input = request.form.get('inputted')
                if field == "id":
                    cur.execute("SELECT * FROM Billets WHERE DataId = ? ", (selected_input,))
                if field == "price":
                    cur.execute("SELECT * FROM Billets WHERE price = ? ", (selected_input,))
                if field == "delivery_time":
                    cur.execute("SELECT * FROM Billets WHERE delivery_time = ? ", (selected_input,))
                if field == "needle_size":
                    cur.execute("SELECT * FROM Billets WHERE needle_size = ? ", (selected_input,))
                if field == "composition":
                    cur.execute("SELECT * FROM Billets WHERE composition = ? ", (selected_input,))
                msg = "Successfully selected"
                rows = cur.fetchall()
        except:
            con.rollback()
            msg = "Failed to select"
            rows = cur.fetchall()
        finally:
            con.close()
            try:
                rows
            except:
                rows = []
            return render_template('list.html', rows = rows , msg=msg)

if __name__ == "__main__":
    app.run(port = 5000,host="0.0.0.0")

