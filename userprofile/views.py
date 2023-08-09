from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UpdateProfileForm
from django.contrib import messages

# Create your views here.
def profile (request, pk):
    user_profile = UserProfile.objects.get(profile_id=pk)
    context = {'profile': user_profile}
    return render(request, 'userprofile/profile.html', context)

def account(request):
    user_account = request.user.userprofile
    context = {'account': user_account}
    return render(request, 'userprofile/account.html', context)

def UpdateProfile(request):
    profile = request.user.userprofile
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Perfil editado exitosamente')
            return redirect ('account')
    context = {'form': form}
    return render(request, 'userprofile/updateprofile.html', context)


def DeleteProfile(request):
    profile = request.user.userprofile
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        profile.delete()
        user = request.user
        user.delete()
        messages.info(request, 'Perfil eliminado exitosamente')
        return redirect('index')
    context = {'form':form}
    return render(request, 'userprofile/deleteprofile.html', context)


