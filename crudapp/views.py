from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Course
from django.contrib import messages
from django.db.models import Q

def index(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    search_query = ""
    
    if request.method == "POST":
        # Student operations
        if "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            course_id = request.POST.get("course")
            
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
            else:
                course = get_object_or_404(Course, id=course_id)
                Student.objects.create(name=name, email=email, course=course)
                messages.success(request, "Student added successfully")
        
        elif "update" in request.POST:
            id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            course_id = request.POST.get("course")
            
            student = get_object_or_404(Student, id=id)
            student.name = name
            student.email = email
            student.course = get_object_or_404(Course, id=course_id)
            student.save()
            messages.success(request, "Student updated successfully")
        
        elif "delete" in request.POST:
            id = request.POST.get("id")
            Student.objects.get(id=id).delete()
            messages.success(request, "Student deleted successfully")
        
        # Course operations
        elif "create_course" in request.POST:
            name = request.POST.get("course_name")
            code = request.POST.get("course_code")
            Course.objects.create(name=name, code=code)
            messages.success(request, "Course added successfully")
        
        elif "update_course" in request.POST:
            id = request.POST.get("course_id")
            name = request.POST.get("course_name")
            code = request.POST.get("course_code")
            course = get_object_or_404(Course, id=id)
            course.name = name
            course.code = code
            course.save()
            messages.success(request, "Course updated successfully")
        
        elif "delete_course" in request.POST:
            id = request.POST.get("course_id")
            Course.objects.get(id=id).delete()
            messages.success(request, "Course deleted successfully")
        

        elif "search" in request.POST:
            search_query = request.POST.get("query", "").strip()
            students = Student.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(course__name__icontains=search_query)
    )
   
    # Enumerate the students, starting from 1
    enumerated_students = list(enumerate(students, start=1))
    enumerated_courses = list(enumerate(courses, start=1)) 
    context = {
        "enumerated_students": enumerated_students, 
        "search_query": search_query,
        "enumerated_courses": enumerated_courses 
    }
    return render(request, "index.html", context=context)
