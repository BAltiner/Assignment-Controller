from Model.model import Teacher
from app import db, create_app
# teachers = Teacher.query.all()
db.session.add(Teacher('x', 'y', 'abcd@gmail.com', 'passw'))
db.create_all(app=create_app())
db.session.commit()