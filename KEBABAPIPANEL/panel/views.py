from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from api.models import Kebab, Suggestion, OpeningHour
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import json
import requests  # Import requests for API calls

# Home: Kebab List View
def kebab_list_view(request):
    kebabs = Kebab.objects.all()
    kebab_hours = []
    for kebab in kebabs:
        opening_hours = kebab.openinghour_set.first()  # Get the first associated opening hours
        if opening_hours:
            kebab_hours.append({
                'kebab_name': kebab.name,
                'hours': opening_hours.hours
            })
    return render(request, 'kebab_list.html', {'kebabs': kebabs, 'kebab_hours': kebab_hours})

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

# New view to display kebab hours
def KebabHoursPanelView(request):
    opening_hours = OpeningHour.objects.all()
    kebab_hours = []
    for hours in opening_hours:
        if hours.hours:  # Check if hours are not None
            kebab_hours.append({
                'kebab_name': hours.kebab.name,
                'hours': hours.hours
            })
    return render(request, 'kebab_hours.html', {'kebab_hours': kebab_hours})

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

@login_required
def edit_hours(request, kebab_id):
    kebab = get_object_or_404(Kebab, id=kebab_id)
    opening_hours = kebab.openinghour_set.first()

    # List of days
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if request.method == 'POST':
        try:
            new_hours = request.POST.get('hours')
            # Check if the hours data is in the correct JSON format
            try:
                new_hours = json.loads(new_hours)
            except json.JSONDecodeError as e:
                return JsonResponse({'status': 'error', 'message': f'Invalid JSON format: {e}'}, status=400)

            # Check if the hours data is a dictionary
            if not isinstance(new_hours, dict):
                return JsonResponse({'status': 'error', 'message': 'Invalid hours format'}, status=400)

            # Check if the hours data contains all the required days
            required_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if set(new_hours.keys()) != set(required_days):
                return JsonResponse({'status': 'error', 'message': 'Invalid hours format'}, status=400)

            # Check if the hours data contains valid times
            for day, times in new_hours.items():
                if not isinstance(times, dict) or 'open' not in times or 'close' not in times:
                    return JsonResponse({'status': 'error', 'message': 'Invalid hours format'}, status=400)
                try:
                    datetime.strptime(times['open'], '%H:%M')
                    datetime.strptime(times['close'], '%H:%M')
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid time format'}, status=400)

            # If the hours data is valid, save it to the database
            if opening_hours is None:
                opening_hours = OpeningHour(kebab=kebab, hours=new_hours)
            else:
                opening_hours.hours = new_hours
            opening_hours.save()
            return redirect('kebab_list')  # Redirect to home page after saving
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Initialize opening_hours if None
    if opening_hours is None:
        opening_hours = {day: {"open": "", "close": ""} for day in days}
    else:
        try:
            # Use the opening_hours.hours attribute directly
            opening_hours = opening_hours.hours
        except AttributeError:
            # If the opening_hours object doesn't have a hours attribute, use a default value
            opening_hours = {day: {"open": "00:00", "close": "00:00"} for day in days}

    # Convert opening_hours to a string before passing it to the JSON editor
    initialData = json.dumps(opening_hours)

    # Render the template with the initial data
    return render(request, 'edit_hours.html', {
        'kebab': kebab,
        'initialData': initialData,
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
