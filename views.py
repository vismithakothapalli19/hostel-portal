from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentRegistrationForm
from .models import Room, Student


@login_required
def home(request):
    students = Student.objects.select_related('room').all()
    total_students = students.count()
    total_rooms = Room.objects.count()

    return render(request, 'home.html', {
        'students': students,
        'total_students': total_students,
        'total_rooms': total_rooms,
    })


@login_required
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm()

    return render(request, 'register_student.html', {'form': form})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistrationForm(instance=student)

    return render(request, 'register_student.html', {
        'form': form,
        'student': student,
        'edit_mode': True,
    })


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        return redirect('home')

    return render(request, 'delete_confirm.html', {'student': student})
