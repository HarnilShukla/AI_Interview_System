from flask import Flask, render_template, request, flash, redirect, session, send_from_directory, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.utils import secure_filename
import os
from datetime import timedelta

app = Flask(__name__)

# === Configuration ===
GROQ_API_KEY = "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"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "thisissecret"

# Upload folder path inside 'mysite/uploads'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['SESSION_PERMANENT'] = False
app.permanent_session_lifetime = timedelta(minutes=30)

# === Setup ===
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# === Models ===
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    domain = db.Column(db.String(100), nullable=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
   

# === Initialize DB ===
with app.app_context():
    db.create_all()

# === Login Loader ===
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === Routes ===

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        domain = request.form.get('domain')
        cv_file = request.files['cv']

        if not username or not password or not cv_file:
            flash('All fields are required!', 'danger')
            return redirect('/register')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'warning')
            return redirect('/register')

        user = User(username=username, password=password, domain=domain)
        db.session.add(user)
        db.session.commit()

        filename = secure_filename(f"{username}_{cv_file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv_file.save(filepath)

        cv_entry = CV(user_id=user.id, filename=filename)
        db.session.add(cv_entry)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect('/login')

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('passWord')

        if username == "admin" and password == "admin":
            return redirect(url_for('admin_dashboard'))

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            session.permanent = False
            return redirect("http://localhost:8501/")
        else:
            flash('Invalid Credentials', 'warning')
            return redirect('/login')

    return render_template("login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    users = User.query.all()
    cvs = {cv.user_id: cv.filename for cv in CV.query.all()}
    admin_user_id = 1
    return render_template("admin_dashboard.html", users=users, cvs=cvs, admin_user_id=admin_user_id)


@app.route("/download_cv/<filename>")
def download_cv(filename):
    try:
        filename = secure_filename(filename)
        uploads_dir = app.config["UPLOAD_FOLDER"]
        file_path = os.path.join(uploads_dir, filename)

        if os.path.exists(file_path):
            return send_from_directory(uploads_dir, filename, as_attachment=True)
        else:
            flash("File not found on server.", "danger")
            return redirect(url_for('admin_dashboard'))

    except Exception as e:
        # This logs the error in error.log
        import traceback
        traceback.print_exc()
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('admin_dashboard'))
    
@app.route('/add_comment/<int:user_id>', methods=['POST'])
def add_comment(user_id):
    comment_text = request.form['comment']
    new_comment = Comment(user_id=user_id, comment=comment_text)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))




# === Run App ===
if __name__ == "__main__":
    app.run(debug=True)