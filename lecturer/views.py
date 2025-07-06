import csv, io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import LecturerProfile, ClassMaterial
from .forms import LecturerClassForm, ClassMaterialForm
from student.models import StudentProfile, Kumpulan, SupervisorRequest
from student.utils import create_default_milestones

@login_required
def lecturer_dashboard(request):
    lecturer_profile, created = LecturerProfile.objects.get_or_create(user=request.user)
    
    #lecturer_profile = LecturerProfile.objects.get(user=request.user)
    supervised_students = SupervisorRequest.objects.filter(lecturer=lecturer_profile, is_approved=True)
    
    return render(request, 'lecturer/dashboard.html', {
        'supervised_students': supervised_students,
    })
    
@login_required
def supervisor_dashboard(request):
    lecturer, created = LecturerProfile.objects.get_or_create(user=request.user)
    
    pending_requests = SupervisorRequest.objects.filter(lecturer=lecturer, is_approved=False)
    approved_students = SupervisorRequest.objects.filter(lecturer=lecturer, is_approved=True)
    
    return render(request, 'lecturer/supervisor.html', {
        'pending_requests': pending_requests,
        'approved_students': approved_students,
    })
    
@login_required
def approve_request(request, request_id):
    supervisor_request = get_object_or_404(SupervisorRequest, id=request_id)
    
    if supervisor_request.lecturer.user == request.user:
        supervisor_request.is_approved = True
        supervisor_request.save()
        
    return redirect('supervisor_dashboard')

@login_required
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        print("got the file")
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Invalid file type. Please upload a .csv file.")
            return redirect('upload_csv')

        data_set = csv_file.read().decode('UTF-8')
        print(data_set)
        io_string = io.StringIO(data_set)
        reader = csv.reader(io_string)

        next(reader, None)
        
        created_count = 0

        for row in reader:
            kumpulan, program, kod_kursus, no_pelajar, nama, fyp_title = [f.strip() for f in row]
            email = f"{no_pelajar}@student.uitm.edu.my"
            
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': no_pelajar, 'first_name': nama}
            )

            kumpulan_instance, _ = Kumpulan.objects.get_or_create(name=kumpulan)
            
            student_profile, prof_created = StudentProfile.objects.get_or_create(user=user)
            
            student_profile.kumpulan = kumpulan_instance
            student_profile.program = program
            student_profile.kod_kursus = kod_kursus
            student_profile.no_pelajar = no_pelajar
            student_profile.nama = nama
            student_profile.fyp_title = fyp_title
            student_profile.save()
            
            if created:
                create_default_milestones(student_profile)

            if prof_created:
                created_count += 1

        messages.success(request, f"{created_count} student profiles successfully created.")
        return redirect('upload_csv')

    return render(request, 'lecturer/upload_csv.html')

@login_required
def select_classes(request):
    profile = LecturerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = LecturerClassForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Classes updated.")
            return redirect('lecturer_dashboard')
    else:
        form = LecturerClassForm(instance=profile)

    return render(request, 'lecturer/select_classes.html', {'form': form})

@login_required
def upload_material(request):
    if request.method == 'POST':
        form = ClassMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('material_list')
    
    else:
        form = ClassMaterialForm()
    return render(request, 'lecturer/upload_material.html', {'form': form})

@login_required
def material_list(request):
    materials = ClassMaterial.objects.all().order_by('-uploaded_at')
    return render(request, 'student/material_list.html', {'materials': materials})

@login_required
def view_student(request):
    lecturer_profile = LecturerProfile.objcets.get(user=request.user)
    students = StudentProfile.objects.filter(kumpulan_in=lecturer_profile.assigned_kumpulan.all())
    return render(request, 'lecturer/view_students.html', {'students': students})

@user_passes_test(lambda u: u.is_superuser)
def library_upload(request):
    return render(request, 'lecturer/upload_library.html')