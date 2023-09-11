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
        # ログインページ, adminページ, トップページへのアクセスは除外
        allowed_paths = [reverse('login'), '/admin/', reverse('top')]
        if request.path not in allowed_paths:
            return HttpResponseRedirect(reverse('top'))
        return None
