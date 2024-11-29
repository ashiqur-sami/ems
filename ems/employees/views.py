from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout


def register_view(request):
    # Redirect logged-in users to home or another page
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('employee_list')  # Replace with your desired redirect URL

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to login after successful registration
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserCreationForm()

    return render(request, 'employees/register.html', {'form': form})


# Login view
def login_view(request):
    # Redirect to home if already logged in
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('employee_list')  # Replace with your desired redirect URL

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('employee_list')  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'employees/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

#helper function
def is_admin(user):
    return user.is_authenticated and user.is_staff  


@login_required(login_url='login')
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.created_by = request.user
            employee.save()
            return redirect('employee_list')  # Make sure this URL name exists
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})
