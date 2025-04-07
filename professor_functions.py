from flask import jsonify, request
from models import *

def get_professor_subjects(professor):
    subjects = [(course.subject.name, course.subject.id) for course in professor.professor_courses]
    return jsonify({"subjects" : subjects}), 200


def fetch_students_in_subject():
    subject_id = request.json.get("subject_id")
    
    if not subject_id:
        return jsonify({"error": "subject_id is required"}), 400

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    students = [
        {
            "reg_no": course.student.reg_no,
            "roll_no": course.student.roll_no,
            "name" : course.student.name
        }
        for course in subject.student_courses
    ]

    return jsonify({
        "subject_id": subject_id,
        "subject_name": subject.name,
        "students": students
    }), 200

def mark_attendance():
    data = request.get_json()
    subject_id = data.get("subject_id")
    student_ids = data.get("student_ids")

    if not subject_id or not isinstance(student_ids, list):
        return jsonify({"error": "Invalid data format"}), 400

    for student_id in student_ids:
        attendance = AttendanceMark.query.filter_by(student_id=student_id, subject_id=subject_id).first()

        if attendance:
            attendance.attendance_count += 1
        else:
            # Create a new attendance record if not exists
            new_attendance = AttendanceMark(student_id=student_id, subject_id=subject_id, attendance_count=1)
            db.session.add(new_attendance)

    db.session.commit()
    return jsonify({"message": "Attendance marked successfully"}), 200

def mark_grade():
    data = request.get_json()
    subject_id = data.get("subject_id")
    grades = data.get("grades")

    if not subject_id or not grades:
        return jsonify({"error": "subject_id and grades are required"}), 400

    for entry in grades:
        student_id = entry.get("student_id")
        grade = entry.get("grade")

        if not student_id or grade is None:
            continue  # Skip invalid entries

        grade_record = GradeMark.query.filter_by(student_id=student_id, subject_id=subject_id).first()

        if grade_record:
            # Update existing grade
            grade_record.grade = grade
        else:
            # Create new grade record
            new_grade = GradeMark(student_id=student_id, subject_id=subject_id, grade=grade)
            db.session.add(new_grade)

    db.session.commit()
    return jsonify({"message": "Grades updated successfully"}), 200





