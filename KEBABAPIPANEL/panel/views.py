from django.shortcuts import render, get_object_or_404, redirect
from api.models import Kebab
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def kebab_list_view(request):
    kebabs = Kebab.objects.all()
    return render(request, 'kebab_list.html', {'kebabs': kebabs})

def kebab_edit_view(request, id):
    kebab = get_object_or_404(Kebab, id=id)
    if request.method == 'POST':
        kebab.name = request.POST.get('name')
        kebab.description = request.POST.get('description')
        kebab.opening_hours = request.POST.get('opening_hours')
        kebab.status = request.POST.get('status')
        kebab.save()
        return redirect('kebab_list')
    return render(request, 'kebab_edit.html', {'kebab': kebab})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/panel/admin')  # Zmień 'home' na nazwę swojej strony głównej
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
