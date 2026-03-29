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
    
    # Get recent notifications (simulated)
    notifications = [
        {"icon": "fa-circle-check", "text": "Session marked as Completed", "time": "Just now"},
        {"icon": "fa-clock", "text": "Study session starts in 10 mins", "time": "10m ago"}
    ]
    
    return render_template('index.html', 
                         plans=plans, 
                         stats={'total': total, 'completed': completed, 'pending': pending},
                         user_name=session.get('user_name'),
                         notifications=notifications)

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

@app.route('/calendar')
@login_required
def calendar():
    user_id = session['user_id']
    plans = list(collection.find({"user_id": user_id}))
    
    # Group plans by day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    calendar_data = {day: [] for day in days}
    for p in plans:
        day = p.get('day', 'Monday')
        if day in calendar_data:
            calendar_data[day].append(p)
            
    return render_template('calendar.html', calendar_data=calendar_data, user_name=session.get('user_name'))

@app.route('/subjects')
@login_required
def subjects():
    user_id = session['user_id']
    plans = list(collection.find({"user_id": user_id}))
    
    # Aggregate subjects
    subject_counts = {}
    for p in plans:
        sub = p.get('subject')
        if sub:
            if sub not in subject_counts:
                subject_counts[sub] = {'total': 0, 'completed': 0}
            subject_counts[sub]['total'] += 1
            if p.get('status') == 'Completed':
                subject_counts[sub]['completed'] += 1
                
    return render_template('subjects.html', subjects=subject_counts, user_name=session.get('user_name'))

@app.route('/analytics')
@login_required
def analytics():
    user_id = session['user_id']
    plans = list(collection.find({"user_id": user_id}))
    
    total = len(plans)
    completed = len([p for p in plans if p.get('status') == 'Completed'])
    
    # Data for Chart.js
    chart_data = {
        'labels': ['Completed', 'Pending'],
        'values': [completed, total - completed]
    }
    
    return render_template('analytics.html', chart_data=chart_data, stats={'total': total, 'completed': completed}, user_name=session.get('user_name'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session['user_id']
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            name = request.form.get('name')
            email = request.form.get('email')
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name, "email": email}})
            session['user_name'] = name
            flash('Profile updated successfully!', 'success')
        elif action == 'change_password':
            old_pass = request.form.get('old_password')
            new_pass = request.form.get('new_password')
            if check_password_hash(user['password'], old_pass):
                users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": generate_password_hash(new_pass)}})
                flash('Password changed successfully!', 'success')
            else:
                flash('Incorrect old password', 'error')
        return redirect(url_for('settings'))
        
    return render_template('settings.html', user=user, user_name=session.get('user_name'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    subject = request.form.get('subject')
    time = request.form.get('time')
    day = request.form.get('day')
    user_id = session['user_id']

    if subject and time:
        collection.insert_one({
            "subject": subject,
            "time": time,
            "day": day,
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