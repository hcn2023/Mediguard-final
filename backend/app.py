from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mediguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    condition = db.Column(db.String(200))

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    medication = db.Column(db.String(100))
    dosage = db.Column(db.String(100))
    taken = db.Column(db.String(10))  # "Yes" or "No"

# Create DB
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    new_user = User(fullname=data['fullname'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'], age=data['age'], condition=data['condition'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added'}), 201

@app.route('/api/view_patients', methods=['GET'])
def view_patients():
    patients = Patient.query.all()
    result = [{'id': p.id, 'name': p.name, 'age': p.age, 'condition': p.condition} for p in patients]
    return jsonify(result), 200

@app.route('/api/add_medication', methods=['POST'])
def add_medication():
    data = request.json
    new_med = Medication(
        patient_id=data['patient_id'],
        medication=data['medication'],
        dosage=data['dosage'],
        taken='No'
    )
    db.session.add(new_med)
    db.session.commit()
    return jsonify({'message': 'Medication added'}), 201

@app.route('/api/view_medications', methods=['GET'])
def view_medications():
    meds = Medication.query.all()
    result = [{
        'id': m.id,
        'patient_id': m.patient_id,
        'medication': m.medication,
        'dosage': m.dosage,
        'taken': m.taken
    } for m in meds]
    return jsonify(result), 200

@app.route('/api/update_medication/<int:med_id>', methods=['PUT'])
def update_medication(med_id):
    data = request.json
    med = Medication.query.get(med_id)
    if med:
        med.taken = data.get('taken', 'No')
        db.session.commit()
        return jsonify({'message': 'Medication status updated'}), 200
    return jsonify({'message': 'Medication not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
