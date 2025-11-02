# 🤖 AI Interview System

## Project Overview

The **AI Interview System** is a Flask-based web application designed to help users enhance their interview skills through an AI-driven platform. It allows users to register, log in, select a domain, and upload their CVs for personalized interview practice. The system includes an administrative dashboard for managing user data, CV downloads, and adding internal comments on user profiles.

This application is tightly integrated with a separate Streamlit application (likely running on `http://localhost:8501/`) for the core AI interview and resume summary functionality.

## ✨ Key Features

* **User Registration & Authentication:** Secure sign-up with username, password, and domain selection.
* **CV Upload:** Users can upload their CV (PDF file) during registration.
* **Domain Selection:** Users choose their professional domain (e.g., Cybersecurity, Data Science) for tailored interviews.
* **Admin Dashboard:** A dedicated dashboard for administrators (`admin/admin` login) to:
    * View all registered users and their selected domains.
    * Download uploaded CVs.
    * Add and delete internal **comments** on user profiles for tracking and communication.
    * Link out to the **Resume Summary App** (Streamlit app).
* **AI Integration (External):** Redirects authenticated non-admin users to the integrated AI interview platform (`http://localhost:8501/`).
* **Session Management:** Uses Flask sessions, configured to be permanent for 30 minutes.

## 🛠️ Technology Stack

* **Backend:** Python, **Flask**
* **Database:** **SQLAlchemy** (using SQLite for simplicity: `project.db`)
* **Frontend:** HTML, **Bootstrap 5.3** (for responsive design and styling)
* **Authentication:** `flask-login`
* **File Handling:** `werkzeug.utils` for secure file uploads.

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

Ensure you have Python installed on your system.

### 2. Clone the Repository (Simulated)

If you had a Git repository, you would clone it here:

```bash
git clone <your-repository-url>
cd AI-Interview-System
