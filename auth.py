from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_manager, login_user, logout_user, current_user, login_required
from Model.model import *
from app import db, bcrypt, login_manager

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/login')
def login():
    return render_template('login.html')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/index')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("çıkış yapıldı")
    return redirect('/index')

# _______________________________________________TEACHER_____________________________________________________________

@auth.route('/Öğretmen Kaydolma', methods=["GET", "POST"])
def t_sign_up():
    name = request.form.get('name')
    mail_address = request.form.get('mail_address')
    t_password = request.form.get('t_password')

    teacher = Teacher.query.filter_by(mail_address=mail_address).first()
    if teacher:
        flash('Mail adrese kayıtlı hesap zaten mevcut!')
        return redirect('t_login')

    new_teacher = Teacher(name=name, mail=mail_address, t_password=t_password)
    db.session.add(new_teacher)
    db.session.commit()
    return redirect('auth.t_login')

# @login_manager.user_loader
# def load_teacher(teacher_id):
#     return Teacher.get_id(teacher_id)

@auth.route('/t_login', methods=["POST"])
def t_login():
    if current_user.is_authenticated:
        return redirect('teacher')
    mail_address = request.form.get('mail_address')
    password = request.form.get('password')

    teacher = Teacher.query.filter_by(mail_address=mail_address).first()
    if not teacher and not bcrypt.check_password_hash(teacher.password, password):
        flash('teacher not exist')
        return redirect('auth.t_login')
    login_user(teacher)
    return redirect('teacher')

@login_manager.user_loader
@login_required
def load_teacher(t_id):
    return Teacher.query.get(int(t_id))

# ________________________________________STUDENT_______________________________________________________________________

@auth.route('/s_login', methods=["POST"])
def s_login():
    if current_user.is_authenticated:
        return redirect('student')
    s_id = request.form.get('s_id')
    password = request.form.get('password')

    student = Student.query.filter_by(id=s_id).first().first()
    if not student and not bcrypt.check_password_hash(student.password, password):
        flash('Student not exist')
        return redirect('auth.t_login')
    login_user(student)
    return redirect('student')


@login_manager.user_loader
@login_required
def load_student(s_id):
    return Student.query.get(int(s_id))

# ____________________________________________ADMIN_________________________________________________________________

@auth.route('/Admin Giriş', methods=['POST'])
def admin_log():
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    admin = Admin.query.filter_by(user_name=user_name).first()
    if not admin and not bcrypt.check_password_hash(admin.password, password):
        flash('Forbidden')
        return redirect('auth.login')
    login_user(admin)
    return redirect('admin')