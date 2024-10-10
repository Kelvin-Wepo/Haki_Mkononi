from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.urls import reverse
from cases.models import Case, Document 



def index(request):
    return render(request, 'index.html')




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("Form submitted")
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            print(f"User created: {user.username}")
            messages.success(request, f'Your account has been created! You can now log in.')
            print("Redirecting to login")
            return redirect('login')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('profile')  # or any other page after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        # Validate forms and save if valid
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        # Initialize forms with the current user's data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,  # Pass the profile instance to the context
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    user_cases = Case.objects.filter(created_by=user)
    
    context = {
        'user_cases_count': user_cases.count(),
        'user_documents_count': Document.objects.filter(case__in=user_cases).count(),
        'notifications_count': 0,  # You'll need to implement a notification system
        'recent_cases': user_cases.order_by('-created_at')[:5],
        'case_categories': Case.CATEGORY_CHOICES,
        'case_list_url': reverse('case_list'),
    }
    
    if hasattr(user, 'profile') and user.profile.role in ['legal_aid', 'admin']:
        context['cases_to_review'] = Case.objects.filter(status='under_review')
    
    return render(request, 'users/dashboard.html', context)