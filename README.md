# 🌱 Green IT Awareness Platform

An interactive educational platform that teaches users about eco-friendly computing practices through quizzes and real-time system monitoring.

----------

## 📦 Project Structure

This project is a full-stack web application developed with:

-   **Backend:** Flask (Python)
    
-   **Frontend:** Tailwind CSS, Chart.js
    
-   **Database:** MongoDB Atlas
    
-   **Live Monitoring:** psutil (Python)
    
-   **Authentication:** Flask sessions & bcrypt
    

Users can learn about Green IT principles through interactive quizzes and observe live CPU and RAM usage during their session.

----------

## 🚀 Getting Started

THIS IS FOR LOCAL DEPLOYMENT IN CASE GLOBAL DEPLOYMENT ON ONLINE SERVER DOES NOT WORK

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/green-it-awareness.git
cd green-it-awareness

```

----------

### 2. Set Up the Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

```

----------

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

----------

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
MONGO_URI=your_mongodb_connection_string

```

----------

### 5. Run the Application

```bash
flask run

```

The app will be available at `http://127.0.0.1:5000/`.

IF THE DEPLOYMENT ON RENDER.COM OR ANY OTHER PLATFORM THAT SUITS THE PROJECT IS SUCCESSFUL, THE URL TO ACCESS THE WEBAPP IS : https://ctrl-save-the-planet.onrender.com

----------

## 📋 Project Overview

### 🔹 Quiz Module

-   Users progress through beginner, intermediate, and advanced levels.
    
-   Each question includes a detailed explanation to promote learning.
    
-   Dynamic difficulty and topic balance using weighted randomization.
    

### 🔹 Real-Time Monitoring Dashboard

-   Live updates of CPU and RAM usage.
    
-   Data is retrieved server-side via **psutil** and pushed every 500ms using AJAX.
    
-   Visualization handled by **Chart.js** with smooth transitions.
    

### 🔹 User Authentication

-   Secure login and registration via Flask sessions.
    
-   Session persistence to track quiz progress.
    

### 🔹 Database

-   MongoDB stores:
    
    -   User profiles
        
    -   Quiz questions and metadata
        
    -   User quiz history and scores
        

### 🔹 Responsive Frontend

-   **Tailwind CSS** for fast, responsive UI development.
   
----------

## 🛠️ Future Development Plans

-   Personalized carbon footprint calculator per device.
    
-   Better looking UX/UI.
    
-   Admin dashboard for moderation and content management.
    
-   Extend monitoring to include GPU and Network usage.
    
-   Implement the live chart on every pages instead of going in a dedicated place.

----------

## Workload Repartition

- Timothée: Live Monitoring, Log In and Register Pages and parts of the Menu and the navbar, Render.com deployment

- Nicolas: Backend with database design (Mongo DB compass and Atlas), navbar adaptability for connection, password hasing, quiz design, Render.com deployment
  
- Matthieu: Caroussel, parts of the menu, report
  
- Julien: Readme.md, prepared the repository for online deployment, prepared the environment and variables, report
  
- Thomas: report, about us page, Render.com deployment

----------

## ✨ Acknowledgements

-   Flask Documentation
    
-   Tailwind CSS Community
    
-   Chart.js Developers
    
-   MongoDB Atlas Team
