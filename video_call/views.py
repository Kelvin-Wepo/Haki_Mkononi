from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VideoCall
from django.contrib.auth.models import User
import uuid

@login_required
def initiate_call(request, official_id):
    # Get the official user object
    official = get_object_or_404(User, id=official_id)
    
    # Check if the user has the correct role to initiate the call
    if request.user.profile.role != 'citizen':
        messages.error(request, "Only citizens can initiate calls with officials.")
        return redirect('case_list')
    
    # Check for ongoing video call
    existing_call = VideoCall.objects.filter(
        user=request.user,
        official=official,
        status='ongoing'
    ).first()
    
    if existing_call:
        return redirect('join_call', room_name=existing_call.room_name)
    
    # If no ongoing call, create a new one
    room_name = str(uuid.uuid4())
    video_call = VideoCall.objects.create(
        user=request.user,
        official=official,
        room_name=room_name,
        status='scheduled'
    )
    
    # Redirect to join the new video call
    return redirect('join_call', room_name=room_name)

@login_required
def join_call(request, room_name):
    video_call = get_object_or_404(VideoCall, room_name=room_name)
    if request.user not in [video_call.user, video_call.official]:
        messages.error(request, "You are not authorized to join this call.")
        return redirect('case_list')
    return render(request, 'video_call/video_call.html', {'room_name': room_name})

@login_required
def call_history(request):
    user_calls = VideoCall.objects.filter(user=request.user)
    official_calls = VideoCall.objects.filter(official=request.user)
    return render(request, 'video_call/call_history.html', {
        'user_calls': user_calls,
        'official_calls': official_calls
    })