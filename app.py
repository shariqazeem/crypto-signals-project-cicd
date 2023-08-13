from flask import Flask, request, jsonify, render_template, session, redirect, url_for, g
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)

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
        user_error_message = "Email already exists. Please use another email address."
        return render_template('signup.html', user_error_message=user_error_message)

    # Check if passwords match
    if password != cpassword:
        user_error_message = "Your passwords do not match. Please try again."
        return render_template('signup.html', user_error_message=user_error_message)

    ## Your signup logic here
    # Insert the new user into the database
    cursor.execute(
        "INSERT INTO users_db (email, password) VALUES (%s, %s)", (email, password))

    mysql.connection.commit()

    cursor.close()
    return redirect(url_for('home'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if the user exists in the database
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT * FROM users_db WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        # If user found, store the user id and email in the session
        session['user_id'] = user[0]
        session['email'] = user[1]
        session['logged_in'] = True
        # Redirect to the home page
        return redirect(url_for('home'))
    else:
        ## If user not found or password doesn't match, display login error message
        login_error_message = "Invalid email or password. Please try again."
        return render_template('login.html', login_error_message=login_error_message)


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')


@app.route('/contact_page')
def contact_page():
    return render_template('contactus.html')


@app.route('/free_signals', methods=['GET'])
def free_signals():
    # Check if the user is logged in
    if 'user_id' in session:
        # Fetch the free signals from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM free_signals")
        free_signals = cursor.fetchall()
        cursor.close()

        # Emit the signals to the client
        socketio.emit('signals_update', free_signals)

        return render_template('free_signals.html', free_signals=free_signals)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('/login_page')

@app.route('/signal_details/<int:signal_sno>', methods=['GET'])
def signal_details(signal_sno):
    if 'user_id' in session:
        # Retrieve the user_id from the session
        user_id = session['user_id']

        # Retrieve the signal details from the database based on signal_sno
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM free_signals WHERE sno = %s", (signal_sno,))
        signal_details = cursor.fetchone()
        cursor.close()

        # Retrieve main comments and their corresponding reply comments from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT c.id, c.comment_text, c.timestamp, c.user_id, "
               "r.id AS reply_id, r.reply_text, r.timestamp AS reply_timestamp, r.user_id AS reply_user_id "
               "FROM comments c "
               "LEFT JOIN replies r ON c.id = r.comment_id "
               "WHERE c.signal_sno = %s", (signal_sno,))


        comments_data = cursor.fetchall()
        cursor.close()

        # Organize the comments and replies into a dictionary
        comments_dict = {}
        for row in comments_data:
            comment_id = row[0]
            if comment_id not in comments_dict:
                comments_dict[comment_id] = {
                    'comment_text': row[1],
                    'comment_timestamp': row[2],
                    'comment_user_id': row[3],
                    'replies': []
                }
            if row[4]:  # If reply exists
                comments_dict[comment_id]['replies'].append({
                    'reply_text': row[5],
                    'reply_timestamp': row[6],
                    'reply_user_id': row[7]
                })

        # Convert the dictionary to a list for template rendering
        comments = list(comments_dict.values())

        return render_template('signal_details.html', signal_details=signal_details, comments=comments, user_id=user_id)
    else:
        return redirect('/login_page')



@app.route('/post_comment', methods=['POST'])
def post_comment():
    # Retrieve data from the form
    signal_sno = request.form['signal_sno']
    user_id = request.form['user_id']
    comment_text = request.form['comment_text']

    # Insert the comment into the database
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO comments (signal_sno, user_id, comment_text) VALUES (%s, %s, %s)",
                   (signal_sno, user_id, comment_text))
    mysql.connection.commit()
    cursor.close()

    # Redirect back to the signal details page to prevent form resubmission
    return redirect(url_for('signal_details', signal_sno=signal_sno, user_id=user_id))

# @app.route('/post_reply', methods=['POST'])
# def post_reply():
#     # Retrieve data from the form
#     signal_sno = request.form['signal_sno']
#     comment_id = request.form['comment_id']  # Make sure you have this field in your form
#     user_id = request.form['user_id']
#     reply_text = request.form['reply_text']

#     # Insert the reply into the database
#     cursor = mysql.connection.cursor()
#     cursor.execute("INSERT INTO replies (comment_id, user_id, reply_text) VALUES (%s, %s, %s)",
#                    (comment_id, user_id, reply_text))
#     mysql.connection.commit()
#     cursor.close()

#     # Redirect back to the signal details page to prevent form resubmission
#     return redirect(url_for('signal_details', signal_sno=signal_sno, user_id=user_id))


@app.route('/home')
def home():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        email = session['email']
        # Customize the header or other parts of the page based on the user's login status
        return render_template('index.html', user_id=user_id, email=email)
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login_page'))
    
@app.template_filter('get_username')
def get_username(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM users_db WHERE id = %s", (user_id,))
    username = cursor.fetchone()[0].split('@')[0]
    cursor.close()
    return username



@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)