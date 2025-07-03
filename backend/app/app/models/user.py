from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey,BLOB,TIMESTAMP,NVARCHAR,Date,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base
from datetime import date,time,timedelta,datetime


class User(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth=Column(Date)
    gender=Column(String(50))
    role=Column(String(255))
    email = Column(String(255))
    password=Column(String(255))
    phone_number = Column(String(50))
    blood_group=Column(String(100))
    mother_tongue=Column(String(100))
    aadhaar_num=Column(String(100))
    is_hosteller=Column(Boolean,default=False)
    specially_abled_person=Column(Boolean,default=False)
    umis_no=Column(String(100))
    father_name=Column(String(100))
    mother_name=Column(String(100))
    parent_phone=Column(String(100))
    emergency_num=Column(String(100))
    date_of_join=Column(Date)
    address_id=Column(Integer,ForeignKey('address.id', use_alter=True, name='fk_users_address_id'),
    nullable=True)
    status = Column(TINYINT,default=1)
    created_at = Column(DateTime,default=datetime.now)
    created_by=Column(Integer,ForeignKey('users.id'))
    modified_at=Column(DateTime,default=datetime.now,onupdate=datetime.now)
    modified_by=Column(Integer,ForeignKey('users.id'))
    
    token=relationship("Apitoken",back_populates="user")
    creator = relationship("User", remote_side=[id], foreign_keys=[created_by], backref="created_users")
    modifier = relationship("User", remote_side=[id], foreign_keys=[modified_by], backref="modified_users")

    created_addresses = relationship("Address", back_populates="creator", foreign_keys="Address.created_by")
    modified_addresses = relationship("Address", back_populates="modifier", foreign_keys="Address.modified_by")

    created_standards = relationship("Standard", back_populates="creator", foreign_keys='Standard.created_by')
    modified_standards = relationship("Standard", back_populates="modifier", foreign_keys='Standard.modified_by')

    created_sections = relationship("Section", back_populates="creator", foreign_keys='Section.created_by')
    modified_sections = relationship("Section", back_populates="modifier", foreign_keys='Section.modified_by')

    advised_classes = relationship("Classroom", back_populates="class_advisor", foreign_keys='Classroom.class_advisor_id')
    created_classrooms = relationship("Classroom", back_populates="creator", foreign_keys='Classroom.created_by')
    modified_classrooms = relationship("Classroom", back_populates="modifier", foreign_keys='Classroom.modified_by')

    created_academic_years = relationship("AcademicYear", back_populates="creator", foreign_keys='AcademicYear.created_by')
    modified_academic_years = relationship("AcademicYear", back_populates="modifier", foreign_keys='AcademicYear.modified_by')

    created_class_academics = relationship("ClassAcademicAssociation", back_populates="creator", foreign_keys='ClassAcademicAssociation.created_by')
    modified_class_academics = relationship("ClassAcademicAssociation", back_populates="modifier", foreign_keys='ClassAcademicAssociation.modified_by')

    created_terms = relationship("Term", back_populates="creator", foreign_keys='Term.created_by')
    modified_terms = relationship("Term", back_populates="modifier", foreign_keys='Term.modified_by')

    created_subjects = relationship("Subject", back_populates="creator", foreign_keys='Subject.created_by')
    modified_subjects = relationship("Subject", back_populates="modifier", foreign_keys='Subject.modified_by')

    created_standard_subject_resources = relationship("SubjectStandardTermResource", back_populates="creator", foreign_keys='SubjectStandardTermResource.created_by')
    modified_standard_subject_resources = relationship("SubjectStandardTermResource", back_populates="modifier", foreign_keys='SubjectStandardTermResource.modified_by')

    subject_allocations = relationship("SubjectAllocation", back_populates="staff",foreign_keys="SubjectAllocation.staff_id")
    created_subject_allocations = relationship("SubjectAllocation", back_populates="creator", foreign_keys='SubjectAllocation.created_by')
    modified_subject_allocations = relationship("SubjectAllocation", back_populates="modifier", foreign_keys='SubjectAllocation.modified_by')

    created_class_academics = relationship("ClassAcademicAssociation", back_populates="creator", foreign_keys="ClassAcademicAssociation.created_by")
    modified_class_academics = relationship("ClassAcademicAssociation", back_populates="modifier", foreign_keys="ClassAcademicAssociation.modified_by")

    created_groups = relationship("Group", back_populates="creator", foreign_keys="Group.created_by")
    modified_groups = relationship("Group", back_populates="modifier", foreign_keys="Group.modified_by")
    
    student_class = relationship("StudentClass", back_populates="student", uselist=False,foreign_keys="StudentClass.student_id")
    created_student_classes = relationship("StudentClass", back_populates="creator", foreign_keys="StudentClass.created_by")
    modified_student_classes = relationship("StudentClass", back_populates="modifier", foreign_keys="StudentClass.modified_by")

    created_exams = relationship("Exam", back_populates="creator", foreign_keys="Exam.created_by")
    modified_exams = relationship("Exam", back_populates="modifier", foreign_keys="Exam.modified_by")

    created_exam_allocations = relationship("ExamAllocation", back_populates="creator", foreign_keys="ExamAllocation.created_by")
    modified_exam_allocations = relationship("ExamAllocation", back_populates="modifier", foreign_keys="ExamAllocation.modified_by")

    marks = relationship("Mark", back_populates="student", foreign_keys="Mark.student_id")
    created_marks = relationship("Mark", back_populates="creator", foreign_keys="Mark.created_by")
    modified_marks = relationship("Mark", back_populates="modifier", foreign_keys="Mark.modified_by")

    attendance_records = relationship("Attendance", back_populates="user", foreign_keys="Attendance.user_id")
    created_attendance_records = relationship("Attendance", back_populates="creator", foreign_keys="Attendance.created_by")
    modified_attendance_records = relationship("Attendance", back_populates="modifier", foreign_keys="Attendance.modified_by")

   
    attendance_records = relationship("Attendance", back_populates="user", foreign_keys="Attendance.user_id")
    created_attendance_records = relationship("Attendance", back_populates="creator", foreign_keys="Attendance.created_by")
    modified_attendance_records = relationship("Attendance", back_populates="modifier", foreign_keys="Attendance.modified_by")

    
    attendance_records = relationship("Attendance",back_populates="user",foreign_keys="Attendance.user_id")
    created_attendance_records = relationship("Attendance",back_populates="creator",foreign_keys="Attendance.created_by")
    modified_attendance_records = relationship("Attendance",back_populates="modifier",foreign_keys="Attendance.modified_by")

    leave_requests = relationship("Leave", back_populates="user", foreign_keys="Leave.user_id")
    created_leave_requests = relationship("Leave", back_populates="creator", foreign_keys="Leave.created_by")
    modified_leave_requests = relationship("Leave", back_populates="modifier", foreign_keys="Leave.modified_by")

    time_table_entries = relationship("TimeTable", back_populates="staff", foreign_keys="TimeTable.staff_id")
    created_time_table_entries = relationship("TimeTable", back_populates="creator", foreign_keys="TimeTable.created_by")
    modified_time_table_entries = relationship("TimeTable", back_populates="modifier", foreign_keys="TimeTable.modified_by")

    created_question_papers = relationship("QuestionPaper", back_populates="creator", foreign_keys="QuestionPaper.created_by")
    modified_question_papers = relationship("QuestionPaper", back_populates="modifier", foreign_keys="QuestionPaper.modified_by")

    
    student_submissions = relationship("StudentSubmission", back_populates="student", foreign_keys="StudentSubmission.student_id")
    created_student_submissions = relationship("StudentSubmission", back_populates="creator", foreign_keys="StudentSubmission.created_by")
    modified_student_submissions = relationship("StudentSubmission", back_populates="modifier", foreign_keys="StudentSubmission.modified_by")

    created_fee_structures = relationship("FeeStructure", foreign_keys="FeeStructure.created_by", back_populates="creator")
    modified_fee_structures = relationship("FeeStructure", foreign_keys="FeeStructure.modified_by", back_populates="modifier")

    
    
    student_fees = relationship("StudentFee", back_populates="student",foreign_keys="StudentFee.student_id")
    created_student_fees = relationship("StudentFee", foreign_keys="[StudentFee.created_by]", back_populates="creator")
    modified_student_fees = relationship("StudentFee", foreign_keys="[StudentFee.modified_by]", back_populates="modifier")
    
    created_fee_payments = relationship("FeePayment", foreign_keys="[FeePayment.created_by]", back_populates="creator")
    modified_fee_payments = relationship("FeePayment", foreign_keys="[FeePayment.modified_by]", back_populates="modifier")

    created_scholarships = relationship("Scholarship", back_populates="creator", foreign_keys="Scholarship.created_by")
    modified_scholarships = relationship("Scholarship", back_populates="modifier", foreign_keys="Scholarship.modified_by")
    student_scholarships = relationship("StudentScholarship", back_populates="student", foreign_keys="StudentScholarship.student_id")

    created_student_scholarships = relationship("StudentScholarship", back_populates="creator", foreign_keys="StudentScholarship.created_by")
    modified_student_scholarships = relationship("StudentScholarship", back_populates="modifier", foreign_keys="StudentScholarship.modified_by")

    organized_events = relationship("Event", back_populates="organizer", foreign_keys='Event.organized_by')
    created_events = relationship("Event", back_populates="creator", foreign_keys='Event.created_by')
    modified_events = relationship("Event", back_populates="modifier", foreign_keys='Event.modified_by')



    


















    
    
    

