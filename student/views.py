from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from .models import StudentProfile, Milestone, Submission, Comment, Kumpulan, SupervisorRequest
from .forms import MilestoneForm, SubmissionForm, CommentForm, SupervisorRequestForm
from .utils import create_default_milestones, list_library_files
import json


@login_required
def student_dashboard(request):
    
    supervisor = None
    fyp_title = None
    default_kumpulan = Kumpulan.objects.first()
    
    StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={'kumpulan': default_kumpulan}
        )
    
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)
    milestones = Milestone.objects.filter(student=student_profile)
    total = milestones.count()
    completed = milestones.filter(is_completed=True).count()
    progress = int((completed / total) * 100) if total > 0 else 0
    stroke_dashoffset = 339.292 - (progress / 100) * 339.292

    if student_profile.kod_kursus == "CSP600":
        if not SupervisorRequest.objects.filter(student=student_profile).exists():
            return redirect('supervisor_request')
    
    request_qs = SupervisorRequest.objects.filter(student=student_profile, is_approved=True).first()
    if request_qs:
        supervisor = request_qs.lecturer
        fyp_title = request_qs.fyp_title
    
    return render(request, 'student/dashboard.html', {
        'student':student_profile,
        'progress':progress,
        'completed':completed,
        'total':total,
        'stroke_dashoffset': stroke_dashoffset,
        'milestones': milestones,
        'supervisor': supervisor,
        'fyp_title': fyp_title,
    })

@csrf_exempt
@login_required
def save_notes(request):
    if request.method == 'POST':
        student = StudentProfile.objects.get(user=request.user)
        notes = request.POST.get('notes', '')
        student.notes = notes
        student.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=404)

@login_required
def milestone_list(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('student_dashboard')
    
    milestones = Milestone.objects.filter(student=student_profile).order_by('due_date')
    crumbs = [
        {"label": "Milestone List", "url": request.path}
    ]
    
    return render(request, 'student/milestone_list.html', {
        'milestones': milestones,
        "crumbs": crumbs,
        })



@login_required
def milestone_add(request):
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.student = student_profile
            last_position = Milestone.objects.filter(student=student_profile).count()
            milestone.position = last_position + 1
            milestone.save()
            return redirect('milestone_list')
    else:
        form = MilestoneForm()
        
    return render(request, 'student/milestone_form.html', {'form':form})

@login_required
def milestone_edit(request,pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            return redirect('milestone_list')
    else:
        form = MilestoneForm(instance=milestone)
        
    return render(request, 'student/milestone_form.html', {
        'form':form, 
        })

@login_required
def milestone_delete(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    milestone.delete()
    return redirect('milestone_list')
        
@login_required
def milestone_toggle(request, pk):
    milestone = get_object_or_404(Milestone, pk=pk)
    milestone.is_completed = not milestone.is_completed
    milestone.save()
    return redirect('milestone_list')

@login_required
def submission_view(request):
    
    student = StudentProfile.objects.get(user=request.user)
    submissions = Submission.objects.filter(student=student)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.save()
            print("Submission saved:", submission.title)
            return redirect('submission')
        else:
            print("Form errors:", form.errors)
    else:
        form = SubmissionForm()
    
    crumbs = [
        {"label": "Submission", "url": request.path}
    ]
    
    return render(request, 'student/submission.html', {
        'form':form,
        'submissions':submissions,
        'crumbs': crumbs,
    })

@login_required
def submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    comments = Comment.objects.filter(submission=submission).order_by('timestamp')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.submission = submission
            comment.author = request.user
            comment.save()
            return redirect('submission_detail', submission_id=submission.id)    
    else:
        form = CommentForm()
        
    crumbs = [
        {"label": "Submission", "url": reverse('submission')},
        {"label": "Submission Details"}
    ]
    return render(request, 'student/submission_detail.html', {
        'submission':submission,
        'comments':comments,
        'form':form
    })

@login_required
def supervisor_request_view(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = SupervisorRequestForm(request.POST)
        if form.is_valid():
            supervisor_request = form.save(commit=False)
            supervisor_request.student = student_profile
            supervisor_request.save()
            return redirect('student_dashboard')
        
    else:
        form = SupervisorRequestForm()
        
    crumbs = [
        {"label": "Supervisor Request", "url": request.path}
    ]
        
    return render(request, 'student/supervisor_request.html', {'form': form}, {'crumbs': crumbs})

@login_required
def student_profile_view(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'student/profile.html', {'student': student_profile})

@login_required
def library_view(request):
    folder_id = "16O889rG1L_R2X3LejzzxlsOn4lhyt24n"
    
    user=request.user
    if hasattr(user, 'studentprofile'):
        role = 'student'
    elif hasattr(user, 'lecturerprofile'):
        role = 'lecturer'
    else:
        role = 'student'
    
    files = list_library_files(folder_id)
    
    crumbs = [
        {"label": "Library", "url": request.path}
    ]
    return render(request, 'student/library.html', {
        'files': files,
        'role':role,
        'crumbs': crumbs,
    })