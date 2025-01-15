from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from api.models import Kebab, Suggestion, OpeningHour
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import json

# Home: Kebab List View
def kebab_list_view(request):
    kebabs = Kebab.objects.all()
    return render(request, 'kebab_list.html', {'kebabs': kebabs})

# Login View
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('kebab_list')  # Redirect to kebab list after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Check Suggestions
@user_passes_test(lambda u: u.is_staff)
def check_suggestions(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'check_suggestions.html', {'suggestions': suggestions})

# Add Suggestion
@login_required
def add_suggestion(request):
    if request.method == 'POST':
        kebab_id = request.POST.get('kebab')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        kebab = get_object_or_404(Kebab, id=kebab_id)
        
        if not description:
            return HttpResponse("Description is required", status=400)
        
        Suggestion.objects.create(user=request.user, kebab=kebab, title=title, description=description)
        return redirect('check_suggestions')
    
    kebabs = Kebab.objects.all()
    return render(request, 'add_suggestion.html', {'kebabs': kebabs})

# Kebab Detail View
def kebab_detail(request, pk):
    kebab = get_object_or_404(Kebab, pk=pk)
    previous_kebab = Kebab.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_kebab = Kebab.objects.filter(pk__gt=pk).order_by('pk').first()
    return render(request, 'kebab_detail.html', {'kebab': kebab, 'previous': previous_kebab, 'next': next_kebab})

# Bulk Opening Hours
@user_passes_test(lambda u: u.is_staff)
def bulk_opening_hours(request):
    if request.method == 'POST':
        hours_data = request.POST.getlist('hours', [])
        for entry in hours_data:
            kebab = get_object_or_404(Kebab, id=entry.get('kebab_id'))
            OpeningHour.objects.update_or_create(
                kebab=kebab,
                defaults={'hours': entry.get('hours')}
            )
        return JsonResponse({'status': 'success', 'message': 'Opening hours updated successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def kebab_opening_hours(request, kebab_id):
    opening_hours = get_object_or_404(OpeningHour, kebab_id=kebab_id)
    hours = json.loads(opening_hours.hours)
    return render(request, 'kebab_hours.html', {'hours': hours})

@login_required
def edit_hours(request, kebab_id):
    kebab = get_object_or_404(Kebab, id=kebab_id)
    opening_hours = kebab.openinghour_set.first()

    # List of days
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if request.method == 'POST':
        try:
            new_hours = json.loads(request.POST.get('hours'))
            opening_hours.hours = new_hours
            opening_hours.save()
            return redirect('kebab_list')  # Redirect to home page after saving
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Initialize opening_hours if None
    if opening_hours is None:
        opening_hours = {day: {"open": "", "close": ""} for day in days}
    else:
        opening_hours = opening_hours.hours

    return render(request, 'edit_hours.html', {
        'kebab': kebab,
        'opening_hours': opening_hours,
        'days': days,
    })

# Get Favorites
@login_required
def get_favorites(request):
    favorites = request.user.favorite_set.all()
    return render(request, 'favorites.html', {'favorites': favorites})

def accept_suggestion(request, suggestion_id):
    if request.method == 'POST':
        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            suggestion.status = 'Accepted'
            suggestion.save()
            return JsonResponse({'status': 'success', 'message': 'Suggestion accepted successfully!'})
        except Suggestion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Suggestion not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def reject_suggestion(request, suggestion_id):
    if request.method == 'POST':
        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            suggestion.status = 'Rejected'
            suggestion.save()
            return JsonResponse({'status': 'success', 'message': 'Suggestion rejected successfully!'})
        except Suggestion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Suggestion not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
