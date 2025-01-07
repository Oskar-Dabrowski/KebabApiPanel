from django.shortcuts import render, get_object_or_404, redirect
from api.models import Kebab, Suggestion
from django.contrib.auth.decorators import login_required
import json

@login_required
def kebab_list_view(request):
    kebabs = Kebab.objects.all()
    return render(request, 'kebab_list.html', {'kebabs': kebabs})

@login_required
def kebab_edit_view(request, id):
    kebab = get_object_or_404(Kebab, id=id)
    if request.method == 'POST':
        kebab.name = request.POST.get('name', kebab.name)
        kebab.description = request.POST.get('description', kebab.description)
        kebab.opening_hours = request.POST.get('opening_hours', kebab.opening_hours)
        kebab.status = request.POST.get('status', kebab.status)
        kebab.save()
        return redirect('kebab_list')
    return render(request, 'kebab_edit.html', {'kebab': kebab})

@login_required
def kebab_detail_view(request, id):
    kebab = get_object_or_404(Kebab, id=id)
    return render(request, 'kebab_detail.html', {'kebab': kebab})

@login_required
def kebab_edit_social_links(request, id):
    kebab = get_object_or_404(Kebab, id=id)
    if request.method == 'POST':
        social_links = request.POST.get('social_links')
        try:
            kebab.social_links = json.loads(social_links)  # Validate JSON input
            kebab.save()
            return redirect('kebab_detail', id=id)
        except ValueError:
            return render(request, 'kebab_edit_social_links.html', {'kebab': kebab, 'error': 'Invalid JSON'})
    return render(request, 'kebab_edit_social_links.html', {'kebab': kebab})

@login_required
def suggestion_list_view(request):
    suggestions = Suggestion.objects.all()
    return render(request, 'suggestion_list.html', {'suggestions': suggestions})

@login_required
def suggestion_accept_view(request, id):
    suggestion = get_object_or_404(Suggestion, id=id)
    suggestion.status = 'Accepted'
    suggestion.save()
    return redirect('suggestion_list')

@login_required
def suggestion_reject_view(request, id):
    suggestion = get_object_or_404(Suggestion, id=id)
    suggestion.status = 'Rejected'
    suggestion.save()
    return redirect('suggestion_list')