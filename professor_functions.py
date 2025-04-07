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




