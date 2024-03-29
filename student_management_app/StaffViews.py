from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .color_generator import generate_colors


from student_management_app.models import CustomUser, Staffs, Group, Subjects, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult


def staff_home(request):
    # Fetching All Students under Staff

    subjects = Subjects.objects.filter(staff_id=request.user.id)
    current_staff = request.user.staffs
    current_staff_groups = current_staff.group_id.all()
    num_of_student = 0
    for group in current_staff_groups:
        num_of_student += group.students_set.count()
    # course_id_list = []
    # for subject in subjects:
    #     course = Courses.objects.get(id=subject.course_id.id)
    #     course_id_list.append(course.id)
    
    # final_course = []
    # Removing Duplicate Course Id
    # for course_id in course_id_list:
    #     if course_id not in final_course:
    #         final_course.append(course_id)
    
    # students_count = Students.objects.filter(course_id__in=final_course).count()
    students_count = num_of_student
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(group_id__in=current_staff_groups).count()
    # Fetch All Approve Leave
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()

    #Fetch Attendance Data by Group
    group_name_list = []
    attendance_list = []
    for group in current_staff_groups:
        attendance_count1 = Attendance.objects.filter(group_id=group.id).count()
        group_name_list.append(group.group_name)
        attendance_list.append(attendance_count1)

    group_name_colors = generate_colors(len(group_name_list))

    students_attendance = Students.objects.all()    # should be fixed
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context={
        "leave_attendance_data": [attendance_count, leave_count],
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "students_count": students_count,
        "subject_count": subject_count,
        "group_name_list": group_name_list,
        "attendance_list": attendance_list,
        "group_name_colors":group_name_colors,
        "student_list": student_list,
        "student_attendance_data": [student_list_attendance_present, student_list_attendance_absent],
    }
    return render(request, "staff_template/staff_home_template.html", context)



def staff_take_attendance(request):
    groups = request.user.staffs.group_id.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "groups":groups,
        "session_years": session_years
    }
    return render(request, "staff_template/take_attendance_template.html", context)


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        if leave_date and leave_message:
            try:
                leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
                leave_report.save()
                messages.success(request, "Tərk etmə üçün müraciət edildi.")
                return redirect('staff_apply_leave')
            except:
                messages.error(request, "Tərk etmə üçün müraciət edərkən xəta baş verdi.")
                return redirect('staff_apply_leave')
        messages.error(request, "Tərk etmə üçün müraciət edərkən xəta baş verdi.")
        return redirect('staff_apply_leave')

def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj).order_by('-updated_at')
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

    if feedback:
        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Rəy göndərildi.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Rəy göndərilərkən xəta baş verdi.")
            return redirect('staff_feedback')
    messages.error(request, "Rəy göndərilərkən xəta baş verdi.")
    return redirect('staff_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    group_id = request.POST.get("group")
    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id

    session_model = SessionYearModel.objects.get(id=session_year)
    group_obj = Group.objects.get(id=group_id)
    students = Students.objects.filter(group_id=group_obj, session_year_id=session_model)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    group_id = request.POST.get("group_id")

    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    group_model = Group.objects.get(id=group_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)

    try:
    # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(group_id=group_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")




def staff_update_attendance(request):
    groups = request.user.staffs.group_id.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "groups": groups,
        "session_years": session_years
    }
    return render(request, "staff_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

    # Getting Values from Ajax POST 'Fetch Student'
    group_id = request.POST.get("group")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    group_model = Group.objects.get(id=group_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(group_id=group_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profil Dəyişdirildi")
            return redirect('staff_profile')
        except:
            messages.error(request, "Profil Dəyişdirilərkən Xəta Baş Verdi")
            return redirect('staff_profile')



def staff_add_result(request):
    groups = request.user.staffs.group_id.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "groups": groups,
        "session_years": session_years,
    }
    return render(request, "staff_template/add_result_template.html", context)


def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        group_id = request.POST.get('group')

        student_obj = Students.objects.get(admin=student_admin_id)
        group_obj = Group.objects.get(id=group_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = StudentResult.objects.filter(group_id=group_id, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(group_id=group_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Nəticə yadda saxlanıldı!")
                return redirect('staff_add_result')
            else:
                result = StudentResult(student_id=student_obj, group_id=group_obj, subject_exam_marks=exam_marks, subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Nəticə yadda saxlanıldı!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Nəticəni yadda saxlayarkən xəta baş verdi!")
            return redirect('staff_add_result')
