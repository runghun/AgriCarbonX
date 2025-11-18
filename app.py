from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL,cursors

app = Flask(__name__)
app.secret_key = "your_secret_key"   # Required for session

# ---- MySQL CONFIG ----
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   # enter your MySQL password here
app.config['MYSQL_DB'] = 'agricarbonx'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password = user[2]  # password column

            if password == stored_password:  # plain text match
                session['username'] = username
                return redirect('/dashboard')
            else:
                return render_template('login.html', error="❌ Incorrect Password")

        return render_template('login.html', error="❌ Username not found")

    return render_template('login.html')


@app.route('/farmer_form')
def farmer_form():
    return render_template("farmer_form.html")

@app.route('/add_farmer', methods=['POST'])
def add_farmer():
    name = request.form['name'].strip()
    village = request.form['village'].strip()

    # Backend validation
    import re
    name_pattern = r'^[A-Za-z ]{3,}$'
    village_pattern = r'^[A-Za-z ]{3,}$'

    if not re.match(name_pattern, name):
        return "Invalid Farmer Name. Only letters and spaces allowed, minimum 3 characters."

    if not re.match(village_pattern, village):
        return "Invalid Village Name. Only letters and spaces allowed, minimum 3 characters."

    # Continue saving to database...




@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    village = request.form['village']
    farm_size = float(request.form['farm_size'])
    trees = int(request.form['trees'])
    organic = request.form['organic']

    # ---- SIMPLE CREDIT FORMULA ----
    credits = (farm_size * 0.8) + (trees * 0.3)
    if organic == "yes":
        credits += 5

    co2_saved = credits * 0.6
    value = credits * 200  # ₹200 per credit (dummy)

    # ---- SAVE TO DATABASE ----
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO farmers (name, village, farm_size, trees, organic, credits, co2_saved, value)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, village, farm_size, trees, organic, credits, co2_saved, value))
    mysql.connection.commit()
    cur.close()

    return render_template("result.html",
                           credits=credits,
                           co2=co2_saved,
                           value=value)

@app.route('/marketplace')
def marketplace():
    cursor = mysql.connection.cursor()
    
    # Fetch farmers with their credits and value
    cursor.execute("""
        SELECT id, name, village, farm_size, trees, organic, credits, co2_saved, value
        FROM farmers
        WHERE credits > 0
    """)
    
    farmers_data = cursor.fetchall()  # Returns a list of tuples
    cursor.close()

    # Convert tuples to dictionary for easier access in Jinja
    farmers = []
    for f in farmers_data:
        farmers.append({
            'id': f[0],
            'name': f[1],
            'village': f[2],
            'farm_size': f[3],
            'trees': f[4],
            'organic': f[5],
            'credits': f[6],
            'co2_saved': f[7],
            'value': f[8]
        })

    return render_template("marketplace.html", farmers=farmers)

# ----payment ----


# ---- DASHBOARD ----

@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor(cursors.DictCursor)

    cur.execute("SELECT * FROM farmers")
    farmers = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total_farmers FROM farmers")
    total_farmers = cur.fetchone()['total_farmers']

    cur.execute("SELECT SUM(credits) AS total_credits FROM farmers")
    total_credits = cur.fetchone()['total_credits']

    cur.execute("SELECT SUM(value) AS total_value FROM farmers")
    total_value = cur.fetchone()['total_value']

    cur.execute("""
        SELECT t.id, f.name AS farmer_name, t.credits_earned, t.credits_used, t.created_at
        FROM transactions t
        JOIN farmers f ON t.farmer_id = f.id
        ORDER BY t.created_at DESC
        LIMIT 10
    """)
    transactions = cur.fetchall() 
    cur.close()

    return render_template('dashboard.html',
                           farmers=farmers,
                           total_farmers=total_farmers,
                           total_credits=total_credits,
                           total_value=total_value,
                           transactions=transactions)

@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    # 1. Get the data submitted from the form (the username or email)
    user_identifier = request.form.get('identifier')
    
    # 2. Look up the user in your database (DB)
    # user = find_user_by_email_or_username(user_identifier)
    
    # 3. IF the user is found:
    #    - Generate a secure token.
    #    - Update the user's record in the DB with the token and expiry time.
    #    - Send the password reset email (usually done after the DB update).
    
    # 4. Return a generic success message to prevent user enumeration attacks
    #    (i.e., don't tell the user if the account exists or not).
    
    return render_template('reset_request_sent.html')

@app.route('/password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Handle password reset logic here
        return "Password reset link sent to your email!"
    return render_template('password.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

from flask import Flask, render_template, request, redirect, url_for, flash

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        farmer_id = request.args.get('farmer_id')

        # Fetch farmer details
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM farmers WHERE id = %s", (farmer_id,))
        farmer = cur.fetchone()
        cur.close()

        if farmer:
            return render_template("payment.html",
                                   farmer_id=farmer[0],
                                   farmer_name=farmer[1],
                                   credits=farmer[6],
                                   value=farmer[8])
        else:
            return "Farmer not found!"

    else:  # POST request
        farmer_id = request.form['farmer_id']
        amount = request.form['amount']
        phone = request.form['phoneNumber']
        email = request.form['Email']
        payment_method = request.form['payment_method']

        # Insert transaction into database (no remarks)
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO transactions (farmer_id, credits_earned, credits_used)
            VALUES (%s, %s, %s)
        """, (farmer_id, 0, 0))  # only farmer_id, credits_earned, credits_used
        mysql.connection.commit()
        cur.close()

        flash("Payment successful and transaction saved!", "success")
        return redirect(url_for('dashboard'))




if __name__ == '__main__':
    app.run(debug=True)
