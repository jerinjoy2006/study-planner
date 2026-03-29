from flask import Flask, render_template, request, redirect, session, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["studyDB"]
collection = db["plans"]
users_collection = db["users"]

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    user_id = session['user_id']
    plans = list(collection.find({"user_id": user_id}))
    
    total = len(plans)
    completed = len([p for p in plans if p.get('status') == 'Completed'])
    pending = total - completed
    
    return render_template('index.html', 
                         plans=plans, 
                         stats={'total': total, 'completed': completed, 'pending': pending},
                         user_name=session.get('user_name'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if users_collection.find_one({"email": email}):
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return redirect(url_for('home'))
            
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    subject = request.form.get('subject')
    time = request.form.get('time')
    user_id = session['user_id']

    if subject and time:
        collection.insert_one({
            "subject": subject,
            "time": time,
            "status": "Pending",
            "user_id": user_id
        })

    return redirect(url_for('home'))

@app.route('/update_status/<id>', methods=['POST'])
@login_required
def update_status(id):
    data = request.get_json()
    new_status = data.get('status')
    if new_status:
        collection.update_one(
            {"_id": ObjectId(id), "user_id": session['user_id']}, 
            {"$set": {"status": new_status}}
        )
        return {"success": True}
    return {"success": False}, 400

@app.route('/api/delete/<id>', methods=['DELETE'])
@login_required
def delete_api(id):
    result = collection.delete_one({"_id": ObjectId(id), "user_id": session['user_id']})
    if result.deleted_count:
        return {"success": True}
    return {"success": False}, 404

if __name__ == '__main__':
    app.run(debug=True)