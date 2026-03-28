from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')

# Connect to MongoDB Atlas using env var
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["studyDB"]
collection = db["plans"]

@app.route('/')
def home():
    # Sort by time or just return list
    plans = list(collection.find())
    return render_template('index.html', plans=plans)

@app.route('/add', methods=['POST'])
def add():
    subject = request.form.get('subject')
    time = request.form.get('time')

    if subject and time:
        collection.insert_one({
            "subject": subject,
            "time": time
        })

    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)