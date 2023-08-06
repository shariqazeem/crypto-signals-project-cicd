from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Sample in-memory data for users (Replace this with database later)
# users = [
#     {"email": "user1@example.com", "password": "password1"},
#     {"email": "user2@example.com", "password": "password2"},
# ]
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "crypto_analysis"

mysql = MySQL(app)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    # Check if the user exists in the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users_db WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "User already exists!"})

    # Check if passwords match
    if password != cpassword:
        return jsonify({"message": "Passwords do not match!"})

    # Your signup logic here
    # Insert the new user into the database
    cursor.execute("INSERT INTO users_db (email, password) VALUES (%s, %s)", (email, password))

    mysql.connection.commit()

    cursor.close()
    return jsonify({"message": "Signup success!"})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if the user exists in the database
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users_db WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login success!"})

    # If user not found or password doesn't match, return login failed message
    return jsonify({"message": "Login failed!"})


@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/contact_page')
def contact_page():
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
