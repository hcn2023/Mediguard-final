import sqlite3
import traceback
from flask import Flask, request, jsonify, send_from_directory, render_template,redirect,flash
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = 'mediguard-secure-2025' 
CORS(app)

# ✅ SQLite Database Connection
db = sqlite3.connect('mediguard.db', check_same_thread=False)
cursor = db.cursor()

# ✅ Create patients table if it doesn’t exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        condition TEXT,
        medication TEXT,
        dosage TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS emergency_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
 

db.commit()

@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()  # <-- For JSON input
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"redirect": "/home.html"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Server error"}), 500










@app.route('/api/emergency_alert', methods=['POST'])
def emergency_alert():
    data = request.get_json()
    alert_type = data.get('type')

    if not alert_type:
        return jsonify({"error": "Missing alert type"}), 400

    query = "INSERT INTO emergency_alerts (type) VALUES (?)"
    cursor.execute(query, (alert_type,))
    db.commit()

    return jsonify({"message": "Emergency alert recorded successfully!"}), 201




# ✅ API route to add a patient
@app.route('/api/add_patient', methods=['POST'])
def add_patient():
    try:
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        condition = data.get('condition')
        medication = data.get('medication')
        dosage = data.get('dosage')

        query = "INSERT INTO patients (name, age, condition, medication, dosage) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (name, age, condition, medication, dosage))
        db.commit()

        return jsonify({"message": "Patient added successfully"}), 201
    except Exception as e:
        print("Error in add_patient:", e)
        return jsonify({"error": "Something went wrong"}), 500

@app.route('/api/mood', methods=['POST'])
def save_mood():
    data = request.get_json()
    mood = data.get('mood')

    if not mood:
        return jsonify({"message": "Mood is required"}), 400

    cursor.execute('CREATE TABLE IF NOT EXISTS mood_log (id INTEGER PRIMARY KEY AUTOINCREMENT, mood TEXT)')
    cursor.execute('INSERT INTO mood_log (mood) VALUES (?)', (mood,))
    db.commit()

    return jsonify({"message": "Mood recorded successfully!"}), 201

# In-memory list to store memory aids (or use a DB if you prefer)
memory_notes = []

@app.route('/api/memory_aid', methods=['POST'])
def save_memory_aid():
    data = request.get_json()
    note = data.get('note')
    if note:
        memory_notes.append(note)
        return jsonify({"message": "Memory note saved!"}), 201
    return jsonify({"message": "Note is empty!"}), 400

@app.route('/emergency_alert.html')
def serve_emergency_alert():
    return send_from_directory('templates', 'emergency_alert.html')



# ✅ API route to view all patients
@app.route('/api/patients', methods=['GET'])
def get_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    patients = []

    for row in rows:
        patient = {
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'condition': row[3],
            'medication': row[4],
            'dosage': row[5]
        }
        patients.append(patient)

    return jsonify(patients)

@app.route('/api/track_medication', methods=['POST'])
def track_medication():
    data = request.get_json()
    taken = data.get('taken')

    # Optional: Save to DB or log (not required now)
    print(f"Medication taken: {taken}")

    return jsonify({"message": "Medication status recorded successfully!"}), 201



        




# ✅ Test Ping
@app.route('/api/ping')
def ping():
    return jsonify({"message": "API is working!"})

@app.route('/view_memory.html')
def serve_view_memory():
    return send_from_directory('templates', 'view_memory.html')

@app.route('/api/memory_aid', methods=['GET'])
def get_memory_notes():
    return jsonify({"notes": memory_notes})

@app.route('/login.html', methods=['GET', 'POST'])
def serve_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect('/home.html')
        else:
            flash("Invalid username or password. Please try again.")
            return redirect('/login.html')

    return render_template('login.html')

@app.route('/home.html')
def serve_home():
    return send_from_directory('templates', 'home.html')




@app.route('/add_patient.html')
def serve_add_patient():
    return send_from_directory('templates', 'add_patient.html')

@app.route('/view_patient.html')
def serve_view_patient():
    return send_from_directory('templates', 'view_patient.html')

@app.route('/mood_tracker.html')
def serve_mood_tracker():
    return send_from_directory('templates', 'mood_tracker.html')

@app.route('/memory_aid.html')
def serve_memory_aid():
    return send_from_directory('templates', 'memory_aid.html')
@app.route('/forgot_password.html')
def serve_forgot_password_page():
    return send_from_directory('templates', 'forgot_password.html')




@app.route('/caregiver_dashboard.html')
def serve_caregiver_dashboard():
    return send_from_directory('templates', 'caregiver_dashboard.html')

@app.route('/medication_tracker.html')
def serve_medication_tracker():
    return send_from_directory('templates', 'medication_tracker.html')

@app.route('/')
def serve_register_page():
    return send_from_directory('templates', 'register.html')

@app.route('/api/forgot_password', methods=['POST'])
def forgot_password():
    try:
        email = request.form.get('email')
        if not email:
            return jsonify({"error": "Email is required"}), 400

        print(f"Password reset requested for: {email}")
        return jsonify({"message": "Password reset instructions sent!"}), 200

    except Exception as e:
        print("Forgot password error:", e)
        return jsonify({"error": "Something went wrong"}), 500




@app.route('/api/medication_tracker', methods=['POST'])
def medication_tracker():
    try:
        data = request.get_json()
        name = data.get('name')
        status = data.get('status')

        if not name or not status:
            return jsonify({"error": "Missing data"}), 400

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medication_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                status TEXT
            )
        ''')
        db.commit()

        # Insert the submitted medication status
        query = "INSERT INTO medication_status (name, status) VALUES (?, ?)"
        cursor.execute(query, (name, status))
        db.commit()

        return jsonify({"message": "Medication status recorded successfully!"}), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong"}), 500

@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([full_name, username, email, password]):
            return jsonify({"error": "All fields are required"}), 400

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                username TEXT,
                email TEXT,
                password TEXT
            )
        ''')

        cursor.execute('''
            INSERT INTO users (full_name, username, email, password)
            VALUES (?, ?, ?, ?)
        ''', (full_name, username, email, password))
        db.commit()

        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        print("Error in registration:", e)
        return jsonify({"error": "Registration failed"}), 500




# ✅ Run Flask App
if __name__ == "__main__":
    try:
        print("✅ Starting Flask server...")
        app.run(debug=True)
    except Exception:
        import traceback
        traceback.print_exc()
