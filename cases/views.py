from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Case, Document
from .forms import CaseForm, DocumentForm
from django.db.models import Q
from django.core.paginator import Paginator
from users.models import Profile
import africastalking  

# import the dotenv module
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

def initialize_africastalking():
    username = os.getenv('AFRICASTALKING_USERNAME')  
    api_key = os.getenv('AFRICASTALKING_API_KEY')    
    africastalking.initialize(username, api_key)

@login_required
def create_case(request):
    if request.method == 'POST':
        case_form = CaseForm(request.POST)
        document_form = DocumentForm(request.POST, request.FILES)
        if case_form.is_valid() and document_form.is_valid():
            case = case_form.save(commit=False)
            case.created_by = request.user
            case.save()
            
            document = document_form.save(commit=False)
            document.case = case
            document.save()

            # Send SMS notification
            initialize_africastalking()
            user_name = request.user.get_full_name()  
            category = case.category  
            # phone_number = request.user.profile.phone_number 

            message = f"Dear {user_name}, your case on {category} has been submitted. We will let you know when the hearing begins."
            sender_id = "20880"  # Sender ID

            try:
                # Send SMS with a specified sender ID
                response = africastalking.SMS.send(message, [phone_number], sender_id=sender_id)
                messages.success(request, 'Your case has been submitted successfully! An SMS has been sent to your phone.')
            except Exception as e:
                messages.error(request, f'Your case has been submitted, but there was an error sending the SMS: {str(e)}')
            
            return redirect('case_detail', pk=case.pk)
    else:
        case_form = CaseForm()
        document_form = DocumentForm()
    return render(request, 'cases/case_form.html', {'case_form': case_form, 'document_form': document_form})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})

@login_required
def case_list(request):
    # Ensure the user has a profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Handle the case where the profile doesn't exist
        profile = Profile.objects.create(user=request.user)

    # Now proceed with the logic based on the user's role
    if profile.role == 'citizen':
        cases = Case.objects.filter(created_by=request.user)
    elif profile.role in ['admin', 'legal_aid']:
        cases = Case.objects.all()
    else:
        cases = Case.objects.none()

    return render(request, 'cases/case_list.html', {'cases': cases})

def case_search(request):
    form = CaseSearchForm(request.GET)
    cases = Case.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')

        if query:
            cases = cases.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(created_by__username__icontains=query)
            )
        
        if category:
            cases = cases.filter(category=category)
        
        if status:
            cases = cases.filter(status=status)

    paginator = Paginator(cases, 10)  # Show 10 cases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'cases/case_search.html', context)
