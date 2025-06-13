from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Table for registered users
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Table for patients
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            condition TEXT,
            medication TEXT,
            dosage TEXT
        )
    ''')

    # Table for medication tracking
    c.execute('''
        CREATE TABLE IF NOT EXISTS medication_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            medication TEXT NOT NULL,
            dosage TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            taken TEXT DEFAULT 'No'
        )
    ''')

    conn.commit()
    conn.close()

   


# --- Landing Page ---
@app.route('/')
def landing():
    return render_template('landing.html')

# --- Register ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (fullname, username, email, password) VALUES (?, ?, ?, ?)",
                  (fullname, username, email, password))
        conn.commit()
        conn.close()

        flash('Registration successful! You can now log in.')
        return redirect('/login')
    return render_template('register.html')

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            flash(f'Login successful! Welcome, {username}', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


# --- Dashboard ---
@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    return render_template('dashboard.html', username=username)

@app.route('/add_tracking', methods=['GET', 'POST'])
def add_tracking():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        medication = request.form['medication']
        dosage = request.form['dosage']
        scheduled_time = request.form['scheduled_time']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO medication_tracking (patient_name, medication, dosage, scheduled_time) VALUES (?, ?, ?, ?)",
                  (patient_name, medication, dosage, scheduled_time))
        conn.commit()
        conn.close()

        flash('Medication tracking added successfully!')
        return redirect('/add_tracking')

       

    return render_template('add_tracking.html')


# --- Add Patient ---
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']
        medication = request.form['medication']
        dosage = request.form['dosage']

        if not name or not age or not condition or not medication or not dosage:
            flash('Please fill in all fields!')
            return redirect('/add_patient')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, condition, medication, dosage) VALUES (?, ?, ?, ?, ?)",
                  (name, age, condition, medication, dosage))
        conn.commit()
        conn.close()

        flash('Patient added successfully!')
        return redirect('/add_patient')

    return render_template('add_patient.html')

# --- View Patients ---
@app.route('/view_patient')
def view_patient():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return render_template('view_patient.html', patients=patients)

@app.route('/view_tracking')
def view_tracking():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM medication_tracking")
    tracking = c.fetchall()
    conn.close()
    return render_template('view_tracking.html', tracking=tracking)

@app.route('/update_taken/<int:id>', methods=['POST'])
def update_taken(id):
    new_status = request.form['taken']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE medication_tracking SET taken = ? WHERE id = ?', (new_status, id))
    conn.commit()
    conn.close()
    flash("✅ Medication status updated successfully!")
    return redirect(url_for('view_tracking'))







# --- Logout ---
@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect('/login')




# --- Main Entry Point ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
