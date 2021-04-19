from flask import redirect, flash, request, Blueprint
from app import db
from flask_login import login_required

auth = Blueprint('auth', __name__)

@auth.route('/create a room', methods=["GET", "POST"])
@login_required
def create_room():
    t_id = request.form.get('t_id')
    room_name = request.form.get('room_name')
    teacher = Teacher.query.filter_by(t_id=t_id)
    if not teacher:
        flash("Teacher not found.")
        return redirect('teacher')
    new_room = Room(room_name)
    db.session.add(new_room)
    db.session.commit()
    return redirect('rooms')

@auth.route('/room deleting', methods=["GET", "POST"])
@login_required
def del_room():
    t_id = request.form.get('t_id')
    room_name = request.form.get('room_name')
    teacher = Teacher.query.filter_by(t_id=t_id)
    if not teacher:
        flash("Teacher not found.")
        return redirect('teacher')
    room_name = Room.query.get(room_name)
    db.session.delete(room_name)
    db.session.commit()

@auth.route('/create an assignment', methods=["GET", "POST"])
@login_required
def create_assignment():
    a_name = request.form.get('a_name')
    due_date = request.form.get('due_date')
    new_assignment = Assignment(a_name, due_date)
    db.session.add(new_assignment)
    db.session.commit()
    return redirect('assignment')

@auth.route('/checking', methods=['GET'])
@login_required
def check_assignment():
    thumbs_up = 1
    thumbs_down = 0
    delivery_id = request.form.get('delivery_id')
    delivered_assignment = Assignment.query.filter_by(delivery_id)
    if delivered_assignment:
        return thumbs_up
    return thumbs_down

@auth.route('/Comment', methods=['POST', 'GET'])
@login_required
def make_comment():
    comment = request.form.get('comment')
    teachers_comment = DeliveredAssignments.query.filter_by(comment_of_teacher=comment)
    if not teachers_comment:
        teachers_comment.comment_of_teacher = comment
        db.session.commit()
        flash("Commented")
        return redirect('profile')
    flash("Commented before")
    return redirect('profile')

@auth.route('/Update Profile', methods=['GET', 'POST'])
@login_required
def update_name():
    teachers_name = request.form.get('teachers_name')
    pass

@auth.route('/Update Profile', methods=['GET', 'POST'])
@login_required
def update_mail():
    teachers_mail = request.form.get('teachers_mail')
    pass

@auth.route('/Update Profile', methods=['GET', 'POST'])
@login_required
def update_password():
    teachers_password = request.form.get('teachers_password')
    pass

@auth.route('Add Student', methods=['GET', 'POST'])
@login_required
def add_student():
    name = request.form.get('student_name')
    password = request.form.get('password')
    student = Student.query.filter_by(name=name, s_password=password)
    if not student:
        db.session.add(student)
        db.session.commit()
        flash("Student added")
        return redirect('room')
    flash("student already exist")
    return redirect('room')
