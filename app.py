from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re  

app = Flask(__name__) 

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sfarm'
  
mysql = MySQL(app)  

@app.route('/', methods =['GET', 'POST'])
def login():
    mesage=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = % s AND PassWord = % s', (username, password, ))
        user = cursor.fetchone()
        if user:            
            session['loggedin'] = True
            session['userid'] = user['U_ID']
            session['UserName'] = user['UserName']
            return redirect(url_for('home'))
        else:
            mesage = 'Tên đăng nhập hoặc mật khẩu không chính xác !'
    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/home", methods =['GET', 'POST'])
def home():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM record WHERE Time IN (SELECT max(Time) FROM record WHERE Date IN(SELECT max(Date) FROM record))')
        record = cursor.fetchall()
        cursor.execute('SELECT Status FROM `pumper` WHERE A_ID = 1')
        status = cursor.fetchall()
        cursor.execute('SELECT * FROM `area`')
        area = cursor.fetchall()     
        return render_template("home.html", record = record, status=status, area=area)
    return redirect(url_for('login'))

@app.route("/signin", methods =['GET', 'POST'])
def signin():
    mesage = ''
    succ=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        userName = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = % s', (userName, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, NULL, NULL, NULL, NULL, NULL, NULL)', (userName, password))
            mysql.connection.commit()
            succ = 'New user created!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('sign_in.html', mesage = mesage,succ=succ)
if __name__ == "__main__":
    app.run(debug=True)