from django.shortcuts import render, get_object_or_404, redirect
from api.models import Kebab, Suggestion
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def kebab_list_view(request):
    kebabs = Kebab.objects.all()
    return render(request, 'kebab_list.html', {'kebabs': kebabs})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('panel/admin/api')  # Zmień 'home' na nazwę swojej strony głównej
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def check_suggestions(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'check_suggestions.html', {'suggestions': suggestions})

def add_suggestion(request):
    if request.method == 'POST':
        # Handle form submission
        kebab_id = request.POST.get('kebab')
        suggestion_text = request.POST.get('suggestion')
        
        # Ensure the kebab exists
        try:
            kebab = Kebab.objects.get(id=kebab_id)
        except Kebab.DoesNotExist:
            return HttpResponse("Kebab not found", status=404)
        
        # Create the suggestion
        Suggestion.objects.create(user=request.user, kebab=kebab, suggestion=suggestion_text)
        return redirect('check_suggestions')  # Redirect to the suggestions list after submission
    
    # Handle GET request (render the form)
    kebabs = Kebab.objects.all()  # Fetch all kebabs for the dropdown
    return render(request, 'add_suggestion.html', {'kebabs': kebabs})