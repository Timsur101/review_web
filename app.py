from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'anton'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Timsur12!",
    database="review_web"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (email, email, password, role)  
            )
            db.commit()
            flash('Регистрация прошла успешно! Пожалуйста, войдите.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Ошибка регистрации: {err}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and user['password'] == password: 
            session['user_id'] = user['id_user']
            session['email'] = user['email']
            session['role'] = user['role']
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверные данные для входа.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cursor.execute("""
        SELECT p.*, u.email AS student_email,
               (SELECT AVG(rating) FROM reviews r WHERE r.project_id = p.id_project) AS avg_rating
        FROM projects p 
        JOIN users u ON p.author_id = u.id_user
    """)
    projects = cursor.fetchall()
    
    for project in projects:
        cursor.execute("SELECT r.*, u.email AS reviewer_email FROM reviews r JOIN users u ON r.reviewer_id = u.id_user WHERE r.project_id = %s", (project['id_project'],))
        project['reviews'] = cursor.fetchall()
    
    return render_template('dashboard.html', projects=projects, role=session['role'])

@app.route('/submit_project', methods=['GET', 'POST'])
def submit_project():
    if 'user_id' not in session or session['role'] != 'student':
        flash('Нет доступа.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        repository_url = request.form['repository_url']
        
        cursor.execute(
            "INSERT INTO projects (title, description, author_id, repository_url) VALUES (%s, %s, %s, %s)",
            (title, description, session['user_id'], repository_url)
        )
        db.commit()
        flash('Проект успешно отправлен!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('submit_project.html')

@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    if 'user_id' not in session or session['role'] != 'admin':
        flash('Нет доступа.', 'danger')
        return redirect(url_for('dashboard'))
    
    cursor.execute("DELETE FROM reviews WHERE project_id = %s", (project_id,))
    cursor.execute("DELETE FROM projects WHERE id_project = %s", (project_id,))
    db.commit()
    flash('Проект успешно удален!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/review_project/<int:project_id>', methods=['GET', 'POST'])
def review_project(project_id):
    if 'user_id' not in session or session['role'] != 'reviewer':
        flash('Нет доступа.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        rating = request.form['rating']
        comment = request.form['comment']
        
        cursor.execute(
            "INSERT INTO reviews (project_id, reviewer_id, rating, comment) VALUES (%s, %s, %s, %s)",
            (project_id, session['user_id'], rating, comment)
        )
        db.commit()
        flash('Отзыв успешно отправлен!', 'success')
        return redirect(url_for('dashboard'))
    
    cursor.execute("SELECT * FROM projects WHERE id_project = %s", (project_id,))
    project = cursor.fetchone()
    return render_template('review_project.html', project=project)

@app.route('/logout')
def logout():
    session.clear()
    flash('Выход выполнен успешно.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)