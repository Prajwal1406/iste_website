from flask import Flask,render_template,request,redirect,session
import os
import mysql.connector
app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(host="sql6.freemysqlhosting.net",user="sql6684031",password = "FsZNSq3urr", database="sql6684031")
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('registration.html')
@app.route('/home')
def index():
    return render_template('index.html')
@app.route('/login_val',methods=['POST'])
def login_val():
    email  = request.form.get('Email')
    password = request.form.get('Password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users= cursor.fetchall()
    print(users)
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user',methods =['POST'])
def add_user():
    fname = request.form.get("fName")
    lname = request.form.get("lName")
    email = request.form.get("uEmail")
    password = request.form.get("uPassword")
    cursor.execute("""
        INSERT INTO `users` (`user_id`,`fname`,`lname`,`email`,`password`) VALUES
                   (NULL,'{}','{}','{}','{}')""".format(fname,lname,email,password))
    conn.commit()
    cursor.execute("""
                    SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id']= myuser[0][0]
    return redirect('/home')
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)