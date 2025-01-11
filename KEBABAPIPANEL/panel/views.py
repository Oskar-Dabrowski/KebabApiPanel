from django.shortcuts import render, get_object_or_404, redirect
from api.models import Kebab, Suggestion, Favorite, UserComment
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required

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
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Ensure the kebab exists
        try:
            kebab = Kebab.objects.get(id=kebab_id)
        except Kebab.DoesNotExist:
            return HttpResponse("Kebab not found", status=404)
        
        # Check if description is not empty
        if not description:
            return HttpResponse("Description is required", status=400)
        
        # Create the suggestion
        Suggestion.objects.create(user=request.user, kebab=kebab, title=title, description=description)
        return redirect('check_suggestions')  # Redirect to the suggestions list after submission
    
    # Handle GET request (render the form)
    kebabs = Kebab.objects.all()  # Fetch all kebabs for the dropdown
    return render(request, 'add_suggestion.html', {'kebabs': kebabs})

@user_passes_test(lambda u: u.is_staff)
def suggestion_list(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'suggestion_list.html', {'suggestions': suggestions})

@user_passes_test(lambda u: u.is_staff)
def suggestion_update(request, pk, action):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    if action == 'accept':
        suggestion.status = 'Accepted'
    elif action == 'reject':
        suggestion.status = 'Rejected'
    suggestion.save()
    return redirect('suggestion_list')\
    
def kebab_detail(request, pk):
    kebab = get_object_or_404(Kebab , pk=pk)
    previous_kebab = Kebab.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_kebab = Kebab.objects.filter(pk__gt=pk).order_by('pk').first()
    return render(request, 'kebab_detail.html', {'kebab': kebab, 'previous': previous_kebab, 'next': next_kebab})

@login_required
def add_favorite(request, pk):
    kebab = Kebab.objects.get(pk=pk)
    Favorite.objects.get_or_create(user=request.user, kebab=kebab)
    return redirect('kebab_detail', pk=pk)

@login_required
def remove_favorite(request, pk):
    try:
        favorite = Favorite.objects.get(user=request.user, kebab_id=pk)
        favorite.delete()
        return redirect('kebab_detail', pk=pk)
    except Favorite.DoesNotExist:
        return redirect('kebab_detail', pk=pk)

@login_required
def add_user_comment(request, pk):
    kebab = Kebab.objects.get(pk=pk)
    text = request.POST.get('text')
    UserComment.objects.create(user=request.user, kebab=kebab, text=text)
    return redirect('kebab_detail', pk=pk)