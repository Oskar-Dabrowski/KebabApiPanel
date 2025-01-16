from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse

class CustomAdminLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.request.user.userprofile.has_changed_password:
            return redirect(reverse('admin:password_change'))
        return response
