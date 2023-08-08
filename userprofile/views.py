from django.shortcuts import render
from .models import UserProfile

# Create your views here.
def profile (request, pk):
    user_profile = UserProfile.objects.get(profile_id=pk)
    context = {'profile': user_profile}
    return render(request, 'userprofile/profile.html', context)