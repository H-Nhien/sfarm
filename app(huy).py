from __future__ import division
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask import g
from flask import Response
from flask import request
import json
import MySQLdb
import math


app = Flask(__name__)
CORS(app)

@app.before_request
def db_connect():
    g.conn = MySQLdb.connect(host='localhost', user='root', passwd='123123123', db='sfarm')
    g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
    g.cursor.close()
    g.conn.close()
    return response

@app.route('/')
def home():
    return redirect(url_for('static', filename='homepage.html'))

@app.route("/statistical_table", methods=['GET', 'POST'])  
def statistical_table():
    sql1 = 'SELECT '
    sql2 = ''
    sql3 = ''
    sql4 = ''

    if request.form('element') == 'Moist': 
        sql3 = ' AVG(MoistData) FROM record WHERE R_ID = ' + request.form('area') + ' AND Date_Time >= ' + request.form('TimeStart') + ' AND Date_Time <= ' + request.form('TimeEnd')
    elif request.form('element') == 'Temp': 
        sql3 = ' AVG(TempData) FROM record WHERE R_ID = ' + request.form('area') + ' AND Date_Time >= ' + request.form('TimeStart') + ' AND Date_Time <= ' + request.form('TimeEnd')
    elif request.form('element') == 'Light': 
        sql3 = ' AVG(LightData) FROM record WHERE R_ID = ' + request.form('area') + ' AND Date_Time >= ' + request.form('TimeStart') + ' AND Date_Time <= ' + request.form('TimeEnd')
    else: 
        sql3 = ' AVG(MoistData), AVG(TempData), AVG(LightData) FROM record WHERE R_ID = ' + request.form('area') + ' AND Date_Time >= ' + request.form('TimeStart') + ' AND Date_Time <= ' + request.form('TimeEnd')

    if request.form('unit') == 'month': 
        sql2 = ' YEAR(Date_Time), MONTH(Date_Time),'
        sql4 = ' GROUP BY YEAR(Date_Time), MONTH(Date_Time);'
    elif request.form('unit') == 'week': 
        sql2 = 'YEAR(Date_Time), WEEK(Date_Time),'
        sql4 = ' GROUP BY YEAR(Date_Time), WEEK(Date_Time);'
    elif request.form('unit') == 'day': 
        sql2 = 'YEAR(Date_Time), DAY(Date_Time),'
        sql4 = ' GROUP BY YEAR(Date_Time), DAY(Date_Time);'
    elif request.form('unit') == 'hour': 
        sql2 = 'YEAR(Date_Time), DAY(Date_Time), HOUR(Date_Time),'
        sql4 = ' GROUP BY YEAR(Date_Time), DAY(Date_Time), HOUR(Date_Time);'

    sql = sql1 + sql2 + sql3 + sql4
    g.cursor.execute(sql)
    record = g.cursor.fetchall()
    sendlist = []
    offset = 0

    if request.form('unit') == 'hour':
        for item in record:
            i = {'offset': offset, 'year': item[0], 'day': item[1], 'hour': item[2], 'value': item[3]}
            sendlist.append(i)
            offset = offset + 1
    
    else :
        for item in record:
            i = {'offset': offset, 'time1': item[0], 'time2': item[1], 'value': item[2]}
            sendlist.append(i)
            offset = offset + 1
    
    data = json.dumps(sendlist)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host ='0.0.0.0', debug=True , port=8080, use_reloader=False)