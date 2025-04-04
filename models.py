from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'professor', 'student', 'assistant'

    student_courses = db.relationship('StudentCourse', back_populates='student', cascade="all, delete-orphan")
    professor_courses = db.relationship('ProfessorCourse', back_populates='professor', cascade="all, delete-orphan")

    attendance_records = db.relationship('AttendanceMark', back_populates='student', cascade="all, delete-orphan")
    grade_records = db.relationship('GradeMark', back_populates='student', cascade="all, delete-orphan")


    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    student_courses = db.relationship('StudentCourse', back_populates='subject', cascade="all, delete-orphan")
    professor_courses = db.relationship('ProfessorCourse', back_populates='subject', cascade="all, delete-orphan")

    attendance_records = db.relationship('AttendanceMark', back_populates='subject', cascade="all, delete-orphan")
    grade_records = db.relationship('GradeMark', back_populates='subject', cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Subject {self.name}>"


class StudentCourse(db.Model):
    __tablename__ = 'student_course'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    student = db.relationship('User', back_populates='student_courses')
    subject = db.relationship('Subject', back_populates='student_courses')

    def __repr__(self):
        return f"<StudentCourse(user_id={self.user_id}, subject_id={self.subject_id}, branch='{self.branch}')>"


class ProfessorCourse(db.Model):
    __tablename__ = 'professor_course'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    professor = db.relationship('User', back_populates='professor_courses')
    subject = db.relationship('Subject', back_populates='professor_courses')

    def __repr__(self):
        return f"<ProfessorCourse(user_id={self.user_id}, subject_id={self.subject_id}, branch='{self.branch}')>"


class AttendanceMark(db.Model):
    __tablename__ = 'attendance_mark'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    attendance_count = db.Column(db.Integer, nullable=False, default=0)

    student = db.relationship('User', back_populates='attendance_records')
    subject = db.relationship('Subject', back_populates='attendance_records')

    def __repr__(self):
        return f"<AttendanceMark(user_id={self.user_id}, subject_id={self.subject_id}, attendance_count={self.attendance_count})>"


class GradeMark(db.Model):
    __tablename__ = 'grade_mark'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    student = db.relationship('User', back_populates='grade_records')
    subject = db.relationship('Subject', back_populates='grade_records')

    def __repr__(self):
        return f"<GradeMark(user_id={self.user_id}, subject_id={self.subject_id}, grade={self.grade})>"
