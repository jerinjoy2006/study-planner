# 🎓 Planner Plus

A modern, responsive study planning application built with **Flask**, **MongoDB Atlas**, and **Tailwind CSS**.

## 🚀 Features
- **Interactive AJAX Dashboard:** Seamless updates without page reloads.
- **Status Tracking:** Mark sessions as "Pending" or "Completed" with real-time stats.
- **Modern UI:** Professional "Clean Corporate" dashboard with Indigo-Slate palette.
- **Add Study Plans:** Organize your subjects and time slots easily.
- **Real-time Storage:** Powered by MongoDB Atlas for persistent data.
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

Academia is ready for deployment on **Render**.

### Is Render Free and Safe?
- **Free:** Yes, Render offers a generous **Free Instance Type** for web services.
- **Safe:** Yes, it is highly secure and provides **Free Automatic SSL (HTTPS)** for your site.
- **Run Forever?** On the free plan, the server will **spin down** (go to sleep) after 15 minutes of inactivity. When someone visits your URL, it will "wake up" (this takes ~30 seconds). It stays available forever, but has that small delay after inactivity.

### Deployment Steps:
1. **Push your code to GitHub.**
2. **Log in to [Render](https://render.com).**
3. **Create a New Web Service:** Connect your GitHub repository.
4. **Settings:**
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. **Environment Variables:**
   - Click the "Environment" tab in Render and add:
     - `MONGO_URI`: (Your MongoDB Atlas connection string)
     - `SECRET_KEY`: (A random long string for session security)
     - `PYTHON_VERSION`: `3.11.0`

---
Built with ❤️ for better productivity.
