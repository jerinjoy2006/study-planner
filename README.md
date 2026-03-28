# 🎓 Planner Plus

A modern, responsive study planning application built with **Flask**, **MongoDB Atlas**, and **Tailwind CSS**.

## 🚀 Features
- **Add Study Plans:** Organize your subjects and time slots easily.
- **Real-time Storage:** Powered by MongoDB Atlas for persistent data.
- **Modern UI:** Clean, responsive design using Tailwind CSS.
- **Delete Functionality:** Remove completed or unwanted plans.
- **Secure:** Uses environment variables for sensitive configuration.

## 🛠️ Tech Stack
- **Backend:** Python / Flask
- **Database:** MongoDB Atlas
- **Frontend:** HTML5, Tailwind CSS, FontAwesome
- **Deployment:** Render / Gunicorn

## 📋 Prerequisites
- Python 3.9+
- MongoDB Atlas Cluster

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd study-planner
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI="your_mongodb_atlas_uri"
   SECRET_KEY="your_secret_key"
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

## 🌐 Deployment on Render

1. Create a new **Web Service** on Render.
2. Connect your GitHub repository.
3. Use the following settings:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Add your `.env` variables in the Render **Environment** tab.

---
Built with ❤️ for better productivity.
