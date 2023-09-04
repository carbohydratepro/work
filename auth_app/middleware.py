# middleware.py

from django.http import HttpResponseRedirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # ログインページやadminページへのアクセスは除外
        if not request.user.is_authenticated and request.path not in [reverse('login'), '/admin/']:
            return HttpResponseRedirect(reverse('login'))
        return None
