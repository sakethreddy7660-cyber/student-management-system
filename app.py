from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'secret123'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bunny766'
app.config['MYSQL_DB'] = 'student_db'

mysql = MySQL(app)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')


# Student Registration
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful")

        return redirect(url_for('login'))

    return render_template('register.html')


# Student Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            session['loggedin'] = True
            session['name'] = user[1]

            return redirect(url_for('dashboard'))

        else:
            flash("Invalid Email or Password")

    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:

        return render_template(
            'dashboard.html',
            name=session['name']
        )

    return redirect(url_for('login'))


# Logout
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)