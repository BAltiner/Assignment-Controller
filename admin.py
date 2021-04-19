from Model.model import *
from flask import flash, request, redirect, Blueprint
from app import db, bcrypt, login_manager, admin
from flask_login import login_required
from flask_user import roles_required
from sqlalchemy import update

auth = Blueprint('auth', __name__)

@auth.route('/add teacher', methods=["GET", "POST"])
@login_required
# @admin_required
def add_teacher():
    f_name = request.form.get('f_name')
    mail_address = request.form.get('mail')
    password = request.form.get('password')

    teacher = Teacher.query.filter_by(name=f_name, mail_address=mail_address, password=password).first()
    if not teacher:
        flash("Teacher not exist")
        return redirect('admin')
    teacher.roles.append(Role(name='teacher'))
    db.session.add(teacher)
    db.session.commit()
    return redirect('admin')

@auth.route('/add student', methods=['POST', 'GET'])
@login_required
def add_student():
    f_name = request.form.get('f_name')
    password = request.form.get('password')
    student = Student.query.filter_by(f_name=f_name, s_password=password)
    if not student:
        db.session.add(student)
        db.session.commit()
        return redirect('admin')

    flash("student already exist")
    return redirect('admin')

@auth.route('/delete teacher', methods=['POST', 'GET'])
@login_required
def delete_teacher():
    f_name = request.form.get('f_name')
    mail_address = request.form.get('mail')
    password = request.form.get('password')
    teacher = Teacher.query.filter_by(name=f_name, mail_address=mail_address, password=password).first()
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        flash("teacher deleted")
        return redirect('admin')
    flash("teacher not exist")
    return redirect('admin')

@auth.route('/delete student', methods=['POST', 'GET'])
@login_required
def delete_student():
    f_name = request.form.get('f_name')
    password = request.form.get('password')
    student = Student.query.filter_by(name=f_name, password=password).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("student deleted")
        return redirect('admin')
    flash("student not exist")
    return redirect('admin')

@auth.route('/Update teachers name', method=['POST', 'GET'])
@login_required
def update_teachers_name():
    teachers_id = request.form.get('teachers_id')
    teachers_name = request.form.get('teachers_name')
    teacher = Teacher.query.filter_by(id=teachers_id)
    if teacher:
        teacher.name = teachers_name
        db.session.commit()
        flash("Teachers name updated")
        return redirect('admin')
    flash("user not found")
    return redirect('admin')

@auth.route('/Update teachers mail', method=['POST', 'GET'])
def update_teachers_mail():
    teachers_id = request.form.get('teachers_id')
    teachers_mail = request.form.get('teachers_mail')
    teacher = Teacher.query.filter_by(id=teachers_id)
    if teacher:
        teacher.mail_address = teachers_mail
        db.session.commit()
        flash("Teachers mail updated")
        return redirect('admin')
    flash("user not found")
    return redirect('admin')

@auth.route('/Update teachers password', method=['POST', 'GET'])
@login_required
def update_teachers_password():
    teachers_id = request.form.get('teachers_id')
    teachers_password = request.form.get('teachers_password')
    teacher = Teacher.query.filter_by(id=teachers_id)
    if teacher:
        teacher.password = bcrypt.generate_password_hash(teachers_password)
        db.session.commit()
        flash("Teachers password updated")
        return redirect('admin')
    flash("user not found")
    return redirect('admin')

@auth.route('/Update student password', method=['POST', 'GET'])
@login_required
def update_student_password():
    student_id = request.form.get('student_id')
    student_password = request.form.get('student_password')
    student = Student.query.filter_by(id=student_id)
    if student:
        student.password = bcrypt.generate_password_hash(student_password)
        db.session.commit()
        flash("Student password updated")
        return redirect('admin')
    flash("user not found")
    return redirect('admin')

