from flask import jsonify
from models import Student, ProfessorCourse

def get_student_courses(student):
    if not student:
        return jsonify({"error": "Student not found"}), 404

    enrolled_info = []
    for course in student.student_courses:
        subject = course.subject
        professor_course = ProfessorCourse.query.filter_by(subject_id=subject.id).first()
        professor_name = professor_course.professor.name if professor_course else "Not Assigned"

        enrolled_info.append({
            "subject_id": subject.id,
            "subject_name": subject.name,
            "professor_name": professor_name
        })

    return jsonify({
        "student_id": student.id,
        "student_name": student.name,
        "enrolled_courses": enrolled_info
    }), 200

def get_student_attendance(student):
    if not student:
        return jsonify({"error": "Student not found"}), 404

    attendance_data = []
    for record in student.attendance_records:
        subject = record.subject
        total_classes = 30 
        percentage = round((record.attendance_count / total_classes) * 100, 2)

        attendance_data.append({
            "subject_id": subject.id,
            "subject_name": subject.name,
            "attendance_count": record.attendance_count,
            "attendance_percentage": f"{percentage}%"
        })

    return jsonify({
        "student_id": student.id,
        "student_name": student.name,
        "attendance": attendance_data
    }), 200

def get_student_grades(student):
    if not student:
        return jsonify({"error": "Student not found"}), 404

    grades_data = []
    for record in student.grade_records:
        subject = record.subject

        grades_data.append({
            "subject_id": subject.id,
            "subject_name": subject.name,
            "grade": record.grade
        })

    return jsonify({
        "student_id": student.id,
        "student_name": student.name,
        "grades": grades_data
    }), 200
