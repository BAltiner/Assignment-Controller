from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/t_profile')
def teacher_profile():
    return render_template('teacher.html')

@main.route('/s_profile')
def student_profile():
    return render_template('student.html')