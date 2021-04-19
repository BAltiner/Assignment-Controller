from Model.model import DeliveredAssignments, Room, Assignment
from app import db
from flask import redirect, request, flash, Blueprint, current_app, send_from_directory
from flask_login import login_required, current_user
import datetime
auth = Blueprint('auth', __name__)

@auth.route('/Assignment Delivery/<path:assignment_file>', methods=['POST', 'GET'])
@login_required
def create_delivery(assignment_file):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        today = datetime.datetime.now()
        due = Assignment.get_due_date()
        valid = due - today
        a = datetime.datetime(2021, 1, 1, 1, 1, 1)
        none = a - a
        if valid >= none:
            # https://pythonise.com/series/learning-flask/sending-files-with-flask
            # return flask.send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
            send_from_directory(app.config['UPLOAD_FOLDER'], assignment_file)
            assignment_file = request.form.get('file')
            new_delivery = DeliveredAssignments(assignment_file)
            db.session.add(new_delivery)
            db.session.commit()
            flash("Assignment delivery is susscesful!")
            return redirect('profile')
        else:
            flash("Assignment date is not valid..")
            return redirect('/assignments')

@auth.route('/join room', methods=["POST"])
@login_required
def join_room():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    else:
        key = request.form.get('key')
        room = Room.query.filter_by(room_key=key).first()
        if room:
            db.session.add(current_user)
            db.session.commit()
            return redirect('auth.student')

        else:
            return redirect('student')
