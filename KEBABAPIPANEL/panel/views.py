from django.shortcuts import render, get_object_or_404, redirect
from api.models import Kebab

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
